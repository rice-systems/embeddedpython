# lib/ffi.py
#
# User accessable portions of the FFI module.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

uint8 = 100
sint8 = 101
uint16 = 102
sint16 = 103
uint32 = 104
sint32 = 105
boolean = 106
void = 200

def wrap(fn, args):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_FFI

    pPmForeign_t pforeign;
    pPmObj_t     pptr, pi;
    pPmTuple_t   pparams;
    uint8_t argtype;
    uint16_t i;
    void *fn;

    uint16_t num_params;

     /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }


    // extract the function pointer, do some sanity checking
    pptr = NATIVE_GET_LOCAL(0);

    if (OBJ_GET_TYPE(pptr) != OBJ_TYPE_INT) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int for function pointer");
        return retval;
    }

    fn = (void *) ((pPmInt_t) pptr)->val;

    if (fn == C_NULL) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "refusing to let you cast a null pointer");
        return retval;
    }

    // extract the parameters tuple, do some more sanity checking
    pparams = (pPmTuple_t) NATIVE_GET_LOCAL(1);
    if (!IS_TUPLE_OBJ((pPmObj_t)pparams))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected tuple of arguments");
        return retval;
    }

    num_params = tuple_getLength(pparams);
    
    if (num_params < 1) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "parameters list must have at least one entry");
        return retval;
    }

    // allocate and populate the object

    retval = foreign_new(num_params, &pforeign);
    PM_RETURN_IF_ERROR(retval);

    pforeign->num_params = num_params;
    pforeign->fn.fn_pointer = fn;

    // pack the tuple arguments into place
    for (i=0; i<num_params; i++)
    {
        retval = tuple_getItem(pparams, i, &pi);

        PM_RETURN_IF_ERROR(retval);

        if (OBJ_GET_TYPE(pi) != OBJ_TYPE_INT)
        {
            PM_RAISE(retval, PM_RET_EX_SYS);
            return retval;
        }

        argtype = ((pPmInt_t) pi)->val;
        pforeign->params[i] = argtype;
    }

    NATIVE_SET_TOS((pPmObj_t)pforeign);
#else
    NATIVE_SET_TOS(PM_NONE);
#endif

    return retval;

    """
    pass

def peek(num):
    """__NATIVE__
    pPmObj_t   paddr;
    int *addr;
    pPmInt_t   pval;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    paddr = NATIVE_GET_LOCAL(0);

    if (OBJ_GET_TYPE(paddr) != OBJ_TYPE_INT) {
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
    }

    addr = (int *) ((pPmInt_t) paddr)->val;

    retval = int_new(*addr, &pval);
    NATIVE_SET_TOS((pPmObj_t) pval);
    return retval;
    """
    pass

