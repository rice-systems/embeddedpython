# lib/thread.py
#
# Functions for getting information about threads.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

def get_self():
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }
    
    NATIVE_SET_TOS((pPmObj_t) RUNNINGTHREAD);
    return retval;
    """
    pass

## takes a thread id and returns None if there is no matching thread id in
## the global list, or the Thread matching the passed in thread id
def get_thread(tid):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;
    int16_t i;
    pPmObj_t rpobj;
    pPmInt_t p_tid;
    int8_t result;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }
    /* If wrong type of arg, raise TypeError */
    parg = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(parg) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong type of argument, expected an int");
        return retval;
    }

    result = obj_compare(parg, (pPmObj_t)(gVmGlobal.prunningThread->ptid));
    if (result == C_EQ) {
        NATIVE_SET_TOS((pPmObj_t)(gVmGlobal.prunningThread));
        return retval;
    }

    for (i = 0; i < gVmGlobal.threadList->length; i++)
    {
        retval = list_getItem(gVmGlobal.threadList, i, &rpobj);
        PM_RETURN_IF_ERROR(retval);
        p_tid = ((pPmThread_t)rpobj)->ptid;
        result = obj_compare(parg, (pPmObj_t)p_tid);
        if (result == C_CMP_ERR)
        {
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "cannot compare these objects");
            return retval;
        }
        if (result == C_EQ)
        {
            NATIVE_SET_TOS(rpobj);
            return retval;
        }
    }
    /* No thread id in the threadlist matches the thread id passed in as an argument */
    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass

#
# Print thread statistics
#
def print_stats():
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }
    
    lib_printf("Thread ID: ");
    obj_print((pPmObj_t)RUNNINGTHREAD->ptid, 1);
    lib_printf("\nBytecodes: %d\nNative calls: %d\n",
                 RUNNINGTHREAD->bytecodes,
                 RUNNINGTHREAD->nativecalls);

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass
    

#
# Runs the given function in a thread sharing the current global namespace
#
def spawn(f, arg=None):
    return _spawn(f, arg)

def _spawn(f, arg):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t pf;
    pPmObj_t parg;
    pPmObj_t pthd; // thread object

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* If arg is not a function, raise TypeError */
    pf = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(pf) != OBJ_TYPE_FXN)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    parg = NATIVE_GET_LOCAL(1);

    retval = thread_addThreadWithArg((pPmFunc_t)pf, parg, &pthd);
    NATIVE_SET_TOS(pthd); // return the actual thread object
    return retval;
    """
    pass


#
# Yield control back to the scheduler
#
def scd_yield():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    RUNNINGTHREAD->interpctrl = INTERP_CTRL_RESCHED;

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass

