# lib/_dict.py
#
# Defines the methods of dictionary objects.
#
# This file is Copyright 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

__name__ = "dict"

class _Autobox:
    def clear(self):
        return clear(self.obj)

    def keys(self):
        return keys(self.obj)

    def has_key(self, k):
        return has_key(self.obj, k)

    def pop(self, k):
        return pop(self.obj, k)

    def values(self):
        return values(self.obj)

def clear(d):
    """__NATIVE__
    pPmDict_t pd;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a dict or wrong number of args, */
    pd = (pPmDict_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(pd) != OBJ_TYPE_DIC) || (NATIVE_GET_NUM_ARGS() != 1))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Clear the contents of the dict */
    retval = dict_clear(pd);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    """
    pass


def keys(d):
    """__NATIVE__
    pPmDict_t pd;
    pPmList_t pl;
    pPmObj_t pk;
    pSeglist_t psl;
    uint16_t i;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a dict or wrong number of args, */
    pd = (pPmDict_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(pd) != OBJ_TYPE_DIC) || (NATIVE_GET_NUM_ARGS() != 1))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Create empty list */
    retval = list_new(&pl);
    PM_RETURN_IF_ERROR(retval);

    /* Iterate through the keys seglist */
    psl = pd->d_keys;
    for (i = 0; i < pd->length; i++)
    {
        /* Get the key and append it to the list */
        retval = seglist_getItem(psl, i, &pk);
        PM_RETURN_IF_ERROR(retval);
        retval = list_append(pl, pk);
        PM_RETURN_IF_ERROR(retval);
    }

    /* Return the list of keys to the caller */
    NATIVE_SET_TOS((pPmObj_t)pl);

    return retval;
    """
    pass


def has_key(d, k):
    return k in keys(d)

def pop(d, k):
    v = d[k]
    _remove(d, k)
    return v

def _remove(d, k):
    """__NATIVE__
    pPmDict_t pd;
    pPmObj_t  pk;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a dict or wrong number of args, */
    pd = (pPmDict_t) NATIVE_GET_LOCAL(0);
    pk = NATIVE_GET_LOCAL(1);
    if ((OBJ_GET_TYPE(pd) != OBJ_TYPE_DIC) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "not a dictionary");
        return retval;
    }

    /* remove key from dictionary */
    retval = dict_delItem(pd, pk);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)PM_NONE);

    return retval;
    """
    pass

def values(d):
    """__NATIVE__
    pPmDict_t pd;
    pPmList_t pl;
    pPmObj_t pv;
    pSeglist_t psl;
    uint16_t i;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a dict or wrong number of args, */
    pd = (pPmDict_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(pd) != OBJ_TYPE_DIC) || (NATIVE_GET_NUM_ARGS() != 1))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Create empty list */
    retval = list_new(&pl);
    PM_RETURN_IF_ERROR(retval);

    /* Iterate through the values seglist */
    psl = pd->d_vals;
    for (i = 0; i < pd->length; i++)
    {
        /* Get the value and append it to the list */
        retval = seglist_getItem(psl, i, &pv);
        PM_RETURN_IF_ERROR(retval);
        retval = list_append(pl, pv);
        PM_RETURN_IF_ERROR(retval);
    }

    /* Return the list of values to the caller */
    NATIVE_SET_TOS((pPmObj_t)pl);

    return retval;
    """
    pass


# :mode=c:
