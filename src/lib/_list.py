# lib/_list.py
#
# Implements list methods.
#
# This file is Copyright 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

__name__ = "list"

class _Autobox:
    def append(self, o):
        return append(self.obj, o)

    def count(self, v):
        return count(self.obj, v)

    def extend(self, s):
        return extend(self.obj, s)

    def index(self, o):
        return index(self.obj, o)

    def insert(self, i, o):
        return insert(self.obj, i, o)

    def pop(self, i=None):
        if i==None:
            return pop(self.obj)
        else:
            return pop(self.obj, i)

    def remove(self, v):
        return remove(self.obj, v)

    def clear(self):
        return clear(self.obj)

def list(iterable = []):
    out = []
    for element in iterable:
        out.append(element)

    return out

#TODO: make this less of a hack.
def clear(l):
    while l:
        pop(l)

def append(l, o):
    """__NATIVE__
    pPmList_t pl;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a list or wrong number of args, */
    pl = (pPmList_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(pl) != OBJ_TYPE_LST) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Append the object to the list */
    retval = list_append(pl, NATIVE_GET_LOCAL(1));

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    """
    pass


def count(l, v):
    c = 0
    for o in l:
        if o == v:
            c = c + 1
    return c


def extend(l, s):
    for i in s:
        append(l, i)


def index(l, o):
    """__NATIVE__
    pPmList_t pl;
    pPmObj_t po;
    pPmInt_t pi;
    PmReturn_t retval = PM_RET_OK;
    uint16_t i;

    /* Raise TypeError if it's not a list or wrong number of args, */
    pl = (pPmList_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(pl) != OBJ_TYPE_LST) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the index of the object in the list */
    po = NATIVE_GET_LOCAL(1);
    retval = list_index(pl, po, &i);

    if (retval == PM_RET_EX_VAL)
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    int_new((int32_t)i, &pi);
    NATIVE_SET_TOS((pPmObj_t)pi);

    return retval;
    """
    pass


def insert(l, i, o):
    """__NATIVE__
    pPmList_t pl;
    pPmObj_t pi;
    pPmObj_t po;
    PmReturn_t retval = PM_RET_OK;
    uint16_t i;

    /*
     * Raise TypeError if wrong number of args, first arg is not a list, or
     * second arg is not an int
     */
    pl = (pPmList_t) NATIVE_GET_LOCAL(0);
    pi = NATIVE_GET_LOCAL(1);
    po = NATIVE_GET_LOCAL(2);
    if ((NATIVE_GET_NUM_ARGS() != 3)
        || (OBJ_GET_TYPE(pl) != OBJ_TYPE_LST)
        || (OBJ_GET_TYPE(pi) != OBJ_TYPE_INT) )
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Insert the object before the given index */
    i = (uint16_t)((pPmInt_t)pi)->val;
    retval = list_insert(pl, i, po);

    if (retval != PM_RET_OK)
    {
        PM_RAISE(retval, PM_RET_EX_SYS);
    }

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    """
    pass


def pop(l, i):
    """__NATIVE__
    pPmList_t pl;
    pPmObj_t pi;
    pPmObj_t po;
    PmReturn_t retval = PM_RET_OK;
    int16_t i;

    /*
     * Raise TypeError if first arg is not a list o second arg is not an int
     * or there are the wrong number of arguments
     */
    pl = (pPmList_t) NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(pl) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pi = NATIVE_GET_LOCAL(1);
    if (NATIVE_GET_NUM_ARGS() == 2)
    {
        if (OBJ_GET_TYPE(pi) != OBJ_TYPE_INT)
        {
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
        }
        i = (uint16_t)((pPmInt_t)pi)->val;
    }
    else
    {
        i = -1;
    }
    if ((NATIVE_GET_NUM_ARGS() < 1) || (NATIVE_GET_NUM_ARGS() > 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the object at the given index */
    retval = list_getItem(pl, i, &po);
    PM_RETURN_IF_ERROR(retval);

    /* Return the object to the caller */
    NATIVE_SET_TOS(po);

    /* Remove the object from the given index */
    retval = list_delItem(pl, i);
    PM_RETURN_IF_ERROR(retval);

    return retval;
    """
    pass


def remove(l, v):
    """__NATIVE__
    pPmList_t pl;
    pPmObj_t pv;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a list or wrong number of args, */
    pl = (pPmList_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(pl) != OBJ_TYPE_LST) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Remove the value from the list */
    pv = NATIVE_GET_LOCAL(1);
    retval = list_remove(pl, pv);
    if (retval != PM_RET_OK)
    {
        PM_RAISE(retval, retval);
    }

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    """
    pass

# :mode=c:
