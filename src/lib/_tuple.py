# lib/_tuple.py
#
# Defines methods for tuples.
#
# This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

__name__ = "tuple"

class _Autobox:
    def index(self, o):
        return index(self.obj, o)
        
def tuple(iterable = []):
    return _tuple(iterable)

def _tuple(iterable):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t   pseq;
    pPmTuple_t ptup;
    pPmObj_t   pitem;
    int16_t    len;
    int16_t    i;

     /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }
    pseq = NATIVE_GET_LOCAL(0);

    /* Find length of iterable */
    retval = seq_getLength(pseq, &len);
    PM_RETURN_IF_ERROR(retval);

    /* Allocate space for tuple */
    retval = tuple_new(len, &ptup);
    PM_RETURN_IF_ERROR(retval);

    /* Build tuple */
    for (i = 0; i < len; i++)
    { 
        retval = seq_getItem(pseq, i, &pitem);
        PM_RETURN_IF_ERROR(retval);

        ptup->items[i] = pitem;
    } 

    NATIVE_SET_TOS((pPmObj_t)ptup);
    return retval;
    """
    pass

def index(t, o):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;
    pPmObj_t parg1;
    int16_t index;
    pPmInt_t r_int;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    parg = NATIVE_GET_LOCAL(0);
    parg1 = NATIVE_GET_LOCAL(1);

    /* If wrong type of arg, raise TypeError */
    if (!IS_TUPLE_OBJ(parg))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    retval = tuple_index((pPmTuple_t)parg, parg1, &index);
    PM_RETURN_IF_ERROR(retval);

    retval = int_new((int32_t)index, &r_int);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)r_int);
    return retval;
    """
    pass
