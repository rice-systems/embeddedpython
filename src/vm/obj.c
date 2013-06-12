/* vm/obj.c
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x0F


/**
 * \file
 * \brief Object Type
 *
 * Object type operations.
 */


#include "pm.h"


/* Returns true if the obj is false */
/* BEFORE FUNCTION IS CALLED: have to check if the object is of type Any,
 * Any has no truthiness and is a type error */
int8_t
obj_isFalse(pPmObj_t pobj)
{
    C_ASSERT(pobj != C_NULL);

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_NON:
            /* None evaluates to false, so return true */
            return C_TRUE;     
            
        case OBJ_TYPE_INT:
            /* Only the integer zero is false */
            return ((pPmInt_t)pobj)->val == 0;

#ifdef HAVE_FLOAT
        case OBJ_TYPE_FLT:
            /* The floats 0.0 and -0.0 are false */
            return (((pPmFloat_t) pobj)->val == 0.0)
                || (((pPmFloat_t) pobj)->val == -0.0);
#endif /* HAVE_FLOAT */

        case OBJ_TYPE_STR:
            /* An empty string is false */
            return ((pPmString_t)pobj)->length == 0;

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
            /* An empty tuple is false */
            return tuple_getLength((pPmTuple_t)pobj) == 0;

        case OBJ_TYPE_LST:
            /* An empty list is false */
            return ((pPmList_t)pobj)->length == 0;

        case OBJ_TYPE_DIC:
            /* An empty dict is false */
            return ((pPmDict_t)pobj)->length == 0;

        case OBJ_TYPE_BOL:
            /* C int zero means false */
            return ((pPmBoolean_t) pobj)->val == 0;

        default:
            /*
             * The following types are always not false:
             * CodeObj, Function, Module, Class, ClassInstance.
             */
            return C_FALSE;
    }
}


/* Returns true if the item is in the container object */
PmReturn_t
obj_isIn(pPmObj_t pobj, pPmObj_t pitem)
{
    PmReturn_t retval = PM_RET_NO;
    pPmObj_t ptestItem;
    int16_t i, len;
    uint8_t c;

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_STR:
            /* Raise a TypeError if item is not a string */
            if ((OBJ_GET_TYPE(pitem) != OBJ_TYPE_STR))
            {
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "non-string search key");
                break;
            }

            /* Empty string is alway present */
            if (((pPmString_t)pitem)->length == 0)
            {
                retval = PM_RET_OK;
                break;
            }

            /* Raise a ValueError if the string is more than 1 char */
            else if (((pPmString_t)pitem)->length != 1)
            {
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "multi-character search key");
                break;
            }

            /* Iterate over string to find char */
            c = ((pPmString_t)pitem)->val[0];
            for (i = 0; i < ((pPmString_t)pobj)->length; i++)
            {
                if (c == ((pPmString_t)pobj)->val[i])
                {                      
                    retval = PM_RET_OK;
                    break;
                }
            }
            break;

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_LST:
        case OBJ_TYPE_SET:
        case OBJ_TYPE_XRA:
            /* Iterate over sequence to find item */
            retval = seq_getLength(pobj, &len);
            PM_RETURN_IF_ERROR(retval);
            retval = PM_RET_NO;
            for (i = 0; i < len; i++)
            {
                retval = seq_getItem(pobj, i, &ptestItem);
                PM_RETURN_IF_ERROR(retval);

                if (obj_isEqual(pitem, ptestItem) == C_EQ)
                {
                    retval = PM_RET_OK;
                    break;
                }
                else
                {
                    retval = PM_RET_NO;
                }
            }
            break;

        case OBJ_TYPE_DIC:
            /* Check if the item is one of the keys of the dict */
	    retval = dict_getItem((pPmDict_t)pobj, pitem, &ptestItem);
            if (retval == PM_RET_EX_KEY)
            {
                retval = PM_RET_NO;
            }
            break;

        default:
            PM_RAISE(retval, PM_RET_EX_TYPE);
            break;
    }

    return retval;
}


int8_t
obj_isEqual(pPmObj_t pobj1, pPmObj_t pobj2)
{
    int8_t result;

    C_ASSERT(pobj1 != C_NULL);
    C_ASSERT(pobj2 != C_NULL);

    /* Check if pointers are same */
    if (pobj1 == pobj2)
    {
        return C_EQ;
    }

    switch (OBJ_GET_TYPE(pobj1))
    {
        case OBJ_TYPE_NON:
            if ((OBJ_GET_TYPE(pobj2) == OBJ_TYPE_NON)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_ANY))
            {
                return C_EQ;
            }
            else
            {
                return C_NEQ;
            }
        
        case OBJ_TYPE_ANY:
            return C_EQ;

        case OBJ_TYPE_BOL:
        case OBJ_TYPE_INT:
            if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_BOL
                || OBJ_GET_TYPE(pobj2) == OBJ_TYPE_INT)
            {
                result = int_compare(pobj1, pobj2);
                if (result == C_EQ)
                {
                    return C_EQ;
                }
                else
                {
                    return C_NEQ;
                }
            }
            else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_ANY)
            {
                return C_EQ;
            }
            else
            {
                return C_NEQ;
            }

#ifdef HAVE_FLOAT
        case OBJ_TYPE_FLT:
        {
            if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_FLT
                || OBJ_GET_TYPE(pobj2) == OBJ_TYPE_INT
                || OBJ_GET_TYPE(pobj2) == OBJ_TYPE_BOL)
            {

                result = float_compare(pobj1, pobj2);
            
                if (result == C_EQ)
                {
                    return C_EQ;
                }
                else
                {
                    return C_NEQ;
                }
            }
            else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_ANY)
            {
                return C_EQ;
            }
            else
            {
                return C_NEQ;
            }
        }
#endif /* HAVE_FLOAT */

        case OBJ_TYPE_STR:
        {
            if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_STR)
            {
                result = string_compare((pPmString_t)pobj1, (pPmString_t)pobj2);
                if (result == C_EQ)
                {
                    return C_EQ;
                }
                else
                {
                    return C_NEQ;
                }
            }
            else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_ANY)
            {
                return C_EQ;
            }
            else 
            {
                return C_NEQ;
            }
        }

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_LST:
        case OBJ_TYPE_SET:
            if ((OBJ_GET_TYPE(pobj2) == OBJ_TYPE_TUP)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_LST)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_SET)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_PTP))
            {
                /* seq_isEqual ensures that pobj1 and pobj2 are the same type */
                return seq_isEqual(pobj1, pobj2);
            }
            else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_ANY)
            {
                return C_EQ;
            }
            else
            {
                return C_NEQ;
            }

        case OBJ_TYPE_DIC:
            /* #17: PyMite does not support Dict comparisons (yet) */
        default:
             return C_CMP_ERR;
    }

    /* All other types would need same pointer to be true */
    return C_NEQ;
}

int8_t
obj_compare(pPmObj_t pobj1, pPmObj_t pobj2)
{
    C_ASSERT(pobj1 != C_NULL);
    C_ASSERT(pobj2 != C_NULL);

    /* Check if pointers are same */
    if (pobj1 == pobj2)
    {
        return C_EQ;
    }

    if ((OBJ_GET_TYPE(pobj1) == OBJ_TYPE_ANY) || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_ANY))
    {
        /* Any is equal to everything */
        return C_EQ;
    }

    /* None is less than everything except itself */
    if ((OBJ_GET_TYPE(pobj1) == OBJ_TYPE_NON) || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_NON))
    {
        if (OBJ_GET_TYPE(pobj1) == OBJ_GET_TYPE(pobj2))
        {
            /* Both are None */
            return C_EQ;
        }
        else if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_NON)
        {
            /* pobj1 is None, pobj2 is not */
            return C_GT;
        }
        else
        {
            /* pobj2 is None, pobj1 is not */
            return C_LT;
        }
    }

    switch(OBJ_GET_TYPE(pobj1))
    {
        case OBJ_TYPE_BOL:
        case OBJ_TYPE_INT:
            if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_BOL 
                || OBJ_GET_TYPE(pobj2) == OBJ_TYPE_INT)
            {
                return int_compare(pobj1, pobj2);
            }
#ifdef HAVE_FLOAT
            else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_FLT)
            {
                return float_compare(pobj1, pobj2);
            }
#endif /* HAVE_FLOAT */
            else
            {
                return C_CMP_ERR;
            }
   
#ifdef HAVE_FLOAT
        case OBJ_TYPE_FLT:
            if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_BOL
                || OBJ_GET_TYPE(pobj2) == OBJ_TYPE_INT
                || OBJ_GET_TYPE(pobj2) == OBJ_TYPE_FLT)
            {
                return float_compare(pobj1, pobj2);
            }
            else
            {
                return C_CMP_ERR;
            }
#endif /* HAVE_FLOAT */

        case OBJ_TYPE_STR:
            if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_STR)
            {
                return string_compare((pPmString_t)pobj1, (pPmString_t)pobj2);
            }
            else
            {
                return C_CMP_ERR;
            }

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_LST:
        case OBJ_TYPE_SET:
            if ((OBJ_GET_TYPE(pobj2) == OBJ_TYPE_TUP)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_LST)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_SET)
                || (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_PTP))
            {
                /* seq_compare checks that pobj1 and pobj2 are the same type */
                return seq_compare(pobj1, pobj2, C_FALSE, C_NULL);
            }
            else 
            {
                return C_CMP_ERR;
            }

        case OBJ_TYPE_DIC:
            /* #17: PyMite does not support Dict comparisons (yet) */
        default:
            return C_CMP_ERR;
    }
}

PmReturn_t
obj_copy(pPmObj_t pobj, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int8_t r_bool;

    C_ASSERT(pobj != C_NULL);

    switch(OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_NON:
            *r_pobj = PM_NONE;
            break;
        
        case OBJ_TYPE_INT:
            retval = int_new(((pPmInt_t)pobj)->val, (pPmInt_t *)r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;

#ifdef HAVE_FLOAT
        case OBJ_TYPE_FLT:
            retval = float_new(((pPmFloat_t)pobj)->val, r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;
#endif /* HAVE_FLOAT */
            
        case OBJ_TYPE_STR:
            retval = string_new((char const *)((pPmString_t)pobj)->val, 
                                ((pPmString_t)pobj)->length, (pPmString_t *)r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;

        case OBJ_TYPE_BOL:
            r_bool = obj_compare(pobj, PM_TRUE);
            if (r_bool == C_EQ)
            {
                *r_pobj = PM_TRUE;
            }
            else
            {
                *r_pobj = PM_FALSE;
            }
            break;

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
            retval = tuple_copy((pPmTuple_t)pobj, (pPmTuple_t *)r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;

        case OBJ_TYPE_COB:
        case OBJ_TYPE_PCO:
            retval = co_copy((pPmCo_t)pobj, (pPmCo_t *)r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;

        case OBJ_TYPE_NOB:
            retval = no_copy((pPmNo_t)pobj, (pPmNo_t *)r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;

#ifdef HAVE_FFI
        case OBJ_TYPE_FOR:
            retval = foreign_copy((pPmForeign_t)pobj, (pPmForeign_t *)r_pobj);
            PM_RETURN_IF_ERROR(retval);
            break;
#endif

        default:
            /* Otherwise raise a TypeError */
            PM_RAISE(retval, PM_RET_EX_TYPE);
            break;
    }

    return retval;
}

PmReturn_t
obj_isPackable(pPmObj_t pobj, int8_t *r_bol, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i;
    pPmObj_t item;
 
    C_ASSERT(pobj != C_NULL);

    switch (OBJ_GET_TYPE(pobj))
    {
        /* These types can be sent/packed into a packtuple */
        case OBJ_TYPE_NON:
        case OBJ_TYPE_INT:
#ifdef HAVE_FLOAT
        case OBJ_TYPE_FLT:
#endif /* HAVE_FLOAT */
        case OBJ_TYPE_STR:
        case OBJ_TYPE_PTP: // already packed
        case OBJ_TYPE_BOL:
        case OBJ_TYPE_PCO: // already packed
            *r_bol = C_TRUE;
            *r_pobj = C_NULL; // no object to return
            break;

        case OBJ_TYPE_TUP: 
            // recursively check all elements of the tuple
            for (i = 0; i < ((pPmTuple_t)pobj)->length; i++)
            {
                retval = tuple_getItem((pPmTuple_t)pobj, i, &item);
                PM_BREAK_IF_ERROR(retval);
                retval = obj_isPackable(item, r_bol, r_pobj);
                if (*r_bol == C_FALSE)
                {
                    break;
                }
            } 
            if (*r_bol == C_TRUE)
            {
                // if the tuple is packable, no object to return
                *r_pobj = C_NULL;
            }
            break;

        case OBJ_TYPE_COB:
            // will be packed and become PCO, not yet implemented
            *r_bol = C_FALSE;
            *r_pobj = pobj; // pobj is the object to return
            break;

        /* These types cannot be sent/packed: */
        case OBJ_TYPE_MOD:
        case OBJ_TYPE_CLO:
        case OBJ_TYPE_FXN:
        case OBJ_TYPE_CLI:
        case OBJ_TYPE_NOB:
        case OBJ_TYPE_THR:
        case OBJ_TYPE_MTH:
        case OBJ_TYPE_LST:
        case OBJ_TYPE_DIC:
        case OBJ_TYPE_XRA:
        case OBJ_TYPE_SET:
        case OBJ_TYPE_FRM:
        case OBJ_TYPE_BLK:
        case OBJ_TYPE_SEG:
        case OBJ_TYPE_SGL:
        case OBJ_TYPE_SQI:
#ifdef HAVE_PROFILER
        case OBJ_TYPE_PRO:
#endif /* HAVE_PROFILER */
            *r_bol = C_FALSE;
            *r_pobj = pobj; // pobj is the object to return
            break;

        default:
            /* Otherwise raise a TypeError */
            PM_RAISE(retval, PM_RET_EX_TYPE);
            break;
    }
    return retval;
}

#ifdef HAVE_PRINT
PmReturn_t
obj_print(pPmObj_t pobj, uint8_t marshallString)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pfunc;

    C_ASSERT(pobj != C_NULL);

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_NON:
            if (!marshallString)
            {
                lib_printf("None");
            }
            break;
        case OBJ_TYPE_ANY:
            lib_printf("Any");
            break;
        case OBJ_TYPE_INT:
            retval = int_print((pPmInt_t)pobj);
            break;
#ifdef HAVE_FLOAT
        case OBJ_TYPE_FLT:
            retval = float_print(pobj);
            break;
#endif /* HAVE_FLOAT */
        case OBJ_TYPE_STR:
            retval = string_print(pobj, marshallString);
            break;
        case OBJ_TYPE_DIC:
	    retval = dict_print((pPmDict_t)pobj);
            break;
        case OBJ_TYPE_LST:
        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_SET:
            retval = seq_print(pobj);
            break;

        case OBJ_TYPE_BOL:
            if (((pPmBoolean_t) pobj)->val == C_TRUE)
            {
                lib_printf("True");
            }
            else
            {
                lib_printf("False");
            }
            break;

        case OBJ_TYPE_THR:
            retval = thread_print((pPmThread_t)pobj);
            break;

#ifdef HAVE_FFI
        case OBJ_TYPE_FOR:
            retval = foreign_print((pPmForeign_t)pobj);
            break;
#endif

        /*
        case OBJ_TYPE_MOD:
        case OBJ_TYPE_FXN:
            if (marshallString)
            {
                lib_printf("'");
            }
            lib_printf("<obj type 0x%02x @ %10p>", OBJ_GET_TYPE(pobj), pobj);
            if (marshallString)
            {
                lib_printf("'");
            }
            lib_printf("\nf_co: %p\n", ((pPmFunc_t)pobj)->f_co);
            lib_printf("f_attrs: %p\n", ((pPmFunc_t)pobj)->f_attrs);
            lib_printf("f_globals: %p\n", ((pPmFunc_t)pobj)->f_globals);
            lib_printf("f_defaultargs: %p\n", ((pPmFunc_t)pobj)->f_defaultargs);
            lib_printf("f_closure: %p\n", ((pPmFunc_t)pobj)->f_closure);
            break;
        */

        case OBJ_TYPE_CLI:
            if (!marshallString)
            {
                /* Try to print the __str__ representation */
                retval = class_getAttr(pobj, CONST__str__, &pfunc);
                if (retval == PM_RET_OK)
                {
                    /* TODO: figure out how to call pfunc here */
                    lib_printf("FIXME: call __str__ method!");
                    break;
                }
                /* No __str__ method, fall through */
            }
            retval = PM_RET_OK;
        case OBJ_TYPE_COB:
        case OBJ_TYPE_MOD:
        case OBJ_TYPE_CLO:
        case OBJ_TYPE_FXN:
        case OBJ_TYPE_NOB:
        case OBJ_TYPE_MTH:
        case OBJ_TYPE_SQI:
        case OBJ_TYPE_XRA:
            if (-1 == lib_printf("<obj type 0x%02x @ %10p>", OBJ_GET_TYPE(pobj), pobj))
            {
                PM_RAISE(retval, PM_RET_EX_IO);
                return retval;
            }                
            break;

        default:
            /* Otherwise raise a TypeError */
            PM_RAISE(retval, PM_RET_EX_TYPE);
            break;
    }
    return retval;
}
#endif /* HAVE_PRINT */


