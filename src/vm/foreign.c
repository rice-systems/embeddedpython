/* vm/foreign.c
 *
 * Implements the foreign object type and foreign function calling.
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x1E

#include "pm.h"

#ifdef HAVE_FFI

#include "ffi.h"
#define MAXARGS 8

int stellarisware_true = 1;
int stellarisware_false = 0;

extern uint32_t platform_indirection_table[];

uint32_t *ffi_indirection_table[] = 
{
    ((uint32_t *)0x01000010), // stellarisware
};

PmReturn_t
foreign_new(uint16_t num_params, pPmForeign_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmForeign_t pforeign = C_NULL;

    /* Allocate a FFI object */
    retval = heap_getChunk(sizeof(PmForeign_t) + sizeof(uint8_t)*(num_params-1), (uint8_t **)r_pobj);
    PM_RETURN_IF_ERROR(retval);

    /* Set foreign type, NULL out the contents */
    pforeign = *r_pobj;
    OBJ_SET_TYPE(pforeign, OBJ_TYPE_FOR);

    (pforeign->fn).fn_pointer = NULL;
    pforeign->num_params = num_params;
    pforeign->indirection_length = 0;

    return retval;
}

PmReturn_t
foreign_copy(pPmForeign_t psrc, pPmForeign_t *pdst) {
    PmReturn_t retval = PM_RET_OK;
    uint16_t i;

    /* Allocate a FFI object */
    retval = heap_getChunk(sizeof(PmForeign_t) + 
        sizeof(uint8_t)*((psrc->num_params)-1), (uint8_t **)pdst);
    PM_RETURN_IF_ERROR(retval);

    // copy the data
    OBJ_SET_TYPE(*pdst, OBJ_TYPE_FOR);

    (*pdst)->fn = psrc->fn;
    (*pdst)->indirection_length = psrc->indirection_length;
    (*pdst)->num_params = psrc->num_params;

    for (i=0; i<psrc->num_params; i++) {
        (*pdst)->params[i] = psrc->params[i];
    }

    return retval;
}


PmReturn_t
foreign_print(pPmForeign_t pforeign)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t i;

    if (pforeign->indirection_length == 0)
    {
        lib_printf("<direct foreign function at 0x%x, args: (", 
            (int) pforeign->fn.fn_pointer);
    }
    else
    {
        lib_printf("<indirect foreign function at [");
        
        for (i=0; i<(pforeign->indirection_length); i++) 
        {
            lib_printf("%d,", (pforeign->fn).path[i]);
        }
        
        lib_printf("], args: (");
    }

    for (i=0; i<(pforeign->num_params); i++) 
    {
        lib_printf("%d,", pforeign->params[i]);
    }
    
    lib_printf(")>");

    return retval;
}

#define FFI_PY_RETURN_TYPE_NONE 0
#define FFI_PY_RETURN_TYPE_INT 1
#define FFI_PY_RETURN_TYPE_BOOL 2

PmReturn_t
foreign_call(pPmForeign_t pcallable, pPmTuple_t args, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;

    ffi_cif cif;
    ffi_type *ffi_args[MAXARGS];
    void *ffi_values[MAXARGS];

    void *fn;
    void **fn_table_pos;
    uint16_t num_args, i;
    uint8_t argtype, rettype;

    void *ffi_return_type;
    uint8_t py_return_type, j;

    // on ARM, this always gets shipped back in a zero/sign extended
    // 32 bit register. as such, we give it a 32-bit place to copy to.
    int return_val = 0;

    // make sure we actually got a properly initialized FFI handle
    if (OBJ_GET_TYPE(pcallable) != OBJ_TYPE_FOR)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    // get the function pointer, possibly indirect
    if (pcallable->indirection_length > 0) {
        // this is a little bit terrifying...
        fn_table_pos = (void **) &ffi_indirection_table;

        for (j=0; j<pcallable->indirection_length; j++)
        {
            fn_table_pos = fn_table_pos + pcallable->fn.path[j];
            fn_table_pos = *fn_table_pos;
        }

        fn = (void *) fn_table_pos;
    }
    else
    {
        fn = (void *) (pcallable->fn).fn_pointer;
    }
    
    // make sure we get something sensible
    if (((uint32_t) fn) > 0xf0000000) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "found obviously bogus function pointer");
        return retval;
    }

    // make sure we got the right number of arguments
    // TODO: maybe make this actually say how many we were expecting?
    num_args = tuple_getLength(args);

    // subtract one from the end of the params tuple for the return type at the end
    if (num_args != (pcallable->num_params)-1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "function passed incorrect number of arguments");
        return retval;
    }

    /* unpack the argument tuple */
    for (i=0; i<num_args; i++) {
        argtype = pcallable->params[i];

        // all the numeric types come from ints...
        if ((argtype >=100) && (argtype <=105))
        {
            // get the argument we were passed
            retval = tuple_getItem(args, i, &parg);
            PM_RETURN_IF_ERROR(retval);

            // make sure it's of a type we can handle
            if (OBJ_GET_TYPE(parg) != OBJ_TYPE_INT)
            {
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
                return retval;
            }

            // add pointers into args and values arrays for libffi
            ffi_values[i] = &(((pPmInt_t) parg)->val);
            switch (argtype)
            {
                case 100:
                    ffi_args[i] = &ffi_type_uint8;
                    break;

                case 101:
                    ffi_args[i] = &ffi_type_sint8;
                    break;

                case 102:
                    ffi_args[i] = &ffi_type_uint16;
                    break;

                case 103:
                    ffi_args[i] = &ffi_type_sint16;
                    break;

                case 104:
                    ffi_args[i] = &ffi_type_uint32;
                    break;

                case 105:
                    ffi_args[i] = &ffi_type_sint32;
                    break;

                default:
                    PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "unsupported argument type in foreign object");
                    return retval;
            }
        }
        else if (argtype == 106)
        {
            // get the argument we were passed
            retval = tuple_getItem(args, i, &parg);
            PM_RETURN_IF_ERROR(retval);

            // make sure it's of a type we can handle
            if (OBJ_GET_TYPE(parg) != OBJ_TYPE_BOL)
            {
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected boolean");
                return retval;
            }

            // add pointers into args and values arrays for libffi
            if (obj_isFalse(parg) == C_TRUE) {
                ffi_values[i] = &stellarisware_false;
            }
            else
            {
                ffi_values[i] = &stellarisware_true;
            }

            ffi_args[i] = &ffi_type_uint8;
        }
        else
        {
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "unsupported argument type in foreign object");
            return retval;
        }
    }

    // figure out the return type, stored at the end of the tuples
    rettype = (pcallable->params)[num_args];

    // all the numeric types come from ints...
    if ((rettype >=100) && (rettype <=105))
    {
        py_return_type = FFI_PY_RETURN_TYPE_INT;
        
        switch (rettype)
        {
            case 100:
                ffi_return_type = &ffi_type_uint8;
                break;

            case 101:
                ffi_return_type = &ffi_type_sint8;
                break;

            case 102:
                ffi_return_type = &ffi_type_uint16;
                break;

            case 103:
                ffi_return_type = &ffi_type_sint16;
                break;

            case 104:
                ffi_return_type = &ffi_type_uint32;
                break;

            case 105:
                ffi_return_type = &ffi_type_sint32;
                break;

            default:
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "unsupported argument type in foreign object");
                return retval;
        }
    }
    else if (rettype == 106)
    {
        ffi_return_type = &ffi_type_uint8;
        py_return_type = FFI_PY_RETURN_TYPE_BOOL;
    }
    else if (rettype == 200)
    {
        ffi_return_type = &ffi_type_void;
        py_return_type = FFI_PY_RETURN_TYPE_NONE;
    }
    else
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "unsupported argument type in foreign object");
        return retval;
    }

    /* Initialize the cif */
    if (ffi_prep_cif(&cif, FFI_DEFAULT_ABI, num_args, ffi_return_type, ffi_args) != FFI_OK) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "ffi_prep_cif failed");
        return retval;
    }
    
    // make the call through FFI
    ffi_call(&cif, fn, &return_val, ffi_values);

    // finally, convert the result into a python object
    if (py_return_type == FFI_PY_RETURN_TYPE_NONE)
    {
        *r_pobj = PM_NONE;
    }
    else if (py_return_type == FFI_PY_RETURN_TYPE_INT)
    {
        retval = int_new(return_val, (pPmInt_t *) r_pobj);
        PM_RETURN_IF_ERROR(retval);
    }
    else if (py_return_type == FFI_PY_RETURN_TYPE_BOOL)
    {
        if (return_val)
        {
            *r_pobj = PM_TRUE;
        }
        else
        {
            *r_pobj = PM_FALSE;
        }
    }
    else
    {
        PM_RAISE(retval, PM_RET_EX_SYS);
        return retval;
    }

    return retval;
}

#endif // HAVE_FFI

