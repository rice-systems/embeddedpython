# lib/_set.py
#
# Defines the set object.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

__name__ = "set"

class _Autobox:
    def add(self, o):
        return add(self.obj, o)

    def discard(self, o):
        return discard(self.obj, o)

    def intersection(self, s1):
        return intersection(self.obj, s1)

    def union(self, s1):
        return union(self.obj, s1)

    def difference(self, s1):
        return difference(self.obj, s1)

    def remove(self, o):
        return remove(self.obj, o)

def set(iterable = []):
    out = _empty_set()
    for element in iterable:
        out.add(element)
    return out

def _empty_set():
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmSet_t pset;

     /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    retval = set_new(&pset);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)pset);
    return retval;

    """
    pass

def add(s, o):
    r"""__NATIVE__
    pPmSet_t ps;
    pPmObj_t po;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a set or wrong number of args, */
    ps = (pPmSet_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(ps) != OBJ_TYPE_SET) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the object to add to the set */
    po = NATIVE_GET_LOCAL(1);

    /* If po is not hashable, raise an error */
    if (OBJ_GET_TYPE(po) > OBJ_TYPE_HASHABLE_MAX)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "argument is unhashable, wrong argument type");
        return retval;
    }

    retval = set_add(ps,po);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass

def discard(s, o):
    r"""__NATIVE__
    pPmSet_t ps;
    pPmObj_t po;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a set or wrong number of args, */
    ps = (pPmSet_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(ps) != OBJ_TYPE_SET) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the object to remove from the set */
    po = NATIVE_GET_LOCAL(1);

    retval = set_discard(ps,po);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass

def intersection(s0, s1):
    r"""__NATIVE__
    pPmSet_t ps0;
    pPmSet_t ps1;
    pPmSet_t preturn;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a set or wrong number of args, */
    ps0 = (pPmSet_t) NATIVE_GET_LOCAL(0);
    ps1 = (pPmSet_t) NATIVE_GET_LOCAL(1);
    if ((OBJ_GET_TYPE(ps0) != OBJ_TYPE_SET) || (NATIVE_GET_NUM_ARGS() != 2)
        || (OBJ_GET_TYPE(ps1) != OBJ_TYPE_SET))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected two sets");
        return retval;
    }

    retval = set_intersection(ps0, ps1, &preturn);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)preturn);
    return retval;
    """
    pass

def union(s0, s1):
    r"""__NATIVE__
    pPmSet_t ps0;
    pPmSet_t ps1;
    pPmSet_t preturn;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a set or wrong number of args, */
    ps0 = (pPmSet_t) NATIVE_GET_LOCAL(0);
    ps1 = (pPmSet_t) NATIVE_GET_LOCAL(1);
    if ((OBJ_GET_TYPE(ps0) != OBJ_TYPE_SET) || (NATIVE_GET_NUM_ARGS() != 2)
        || (OBJ_GET_TYPE(ps1) != OBJ_TYPE_SET))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected two sets");
        return retval;
    }

    retval = set_union(ps0, ps1, &preturn);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)preturn);
    return retval;
    """
    pass

def difference(s0, s1):
    r"""__NATIVE__
    pPmSet_t ps0;
    pPmSet_t ps1;
    pPmSet_t preturn;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a set or wrong number of args, */
    ps0 = (pPmSet_t) NATIVE_GET_LOCAL(0);
    ps1 = (pPmSet_t) NATIVE_GET_LOCAL(1);
    if ((OBJ_GET_TYPE(ps0) != OBJ_TYPE_SET) || (NATIVE_GET_NUM_ARGS() != 2)
        || (OBJ_GET_TYPE(ps1) != OBJ_TYPE_SET))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected two sets");
        return retval;
    }

    retval = set_difference(ps0, ps1, &preturn);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)preturn);
    return retval;
    """
    pass

def remove(s, o):
    r"""__NATIVE__
    pPmSet_t ps;
    pPmObj_t po;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a set or wrong number of args, */
    ps = (pPmSet_t) NATIVE_GET_LOCAL(0);
    if ((OBJ_GET_TYPE(ps) != OBJ_TYPE_SET) || (NATIVE_GET_NUM_ARGS() != 2))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the object to remove from the set */
    po = NATIVE_GET_LOCAL(1);

    retval = set_remove(ps,po);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass
