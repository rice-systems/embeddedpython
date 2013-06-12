# lib/_thd.py
#
# Implements thread objects.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

__name__ = "thd"

class _Autobox:
    def get_tid(self):
        return get_tid(self.obj)

    def die(self):
        return die(self.obj)

## Get the thread id corresponding to the passed in thread (s)
def get_tid(s):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments, expected one argument");
        return retval;
    }
    
    parg = NATIVE_GET_LOCAL(0);

    /* If wrong type of arg, raise TypeError */
    if (OBJ_GET_TYPE(parg) != OBJ_TYPE_THR)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong type of argument, expected a thread");
        return retval;
    }

    NATIVE_SET_TOS((pPmObj_t)(((pPmThread_t)parg)->ptid));
    return retval;
    """
    pass
   
def die(s):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments, expected one argument");
        return retval;
    }
    
    parg = NATIVE_GET_LOCAL(0);

    /* If wrong type of arg, raise TypeError */
    if (OBJ_GET_TYPE(parg) != OBJ_TYPE_THR)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong type of argument, expected a thread");
        return retval;
    }

    ((pPmThread_t)parg)->interpctrl = INTERP_CTRL_EXIT;

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass
