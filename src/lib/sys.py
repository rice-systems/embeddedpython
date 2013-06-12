# lib/sys.py
#
# Functions to access and modify the core interpreter.
#
# This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

r"""__NATIVE__
PmReturn_t sleepfn(pPmObj_t *tos);
PmReturn_t getbfn(pPmObj_t *tos);


PmReturn_t sleepfn(pPmObj_t *tos)
{
    uint32_t target_time, now;

    /* TOS contains the time to sleep until */
    target_time = ((pPmInt_t)*tos)->val;

    /* Current time */
    plat_getMsTicks(&now);
    
    if (now < target_time)
    {
        /* Yield and wait */
        RUNNINGTHREAD->interpctrl = INTERP_CTRL_CYIELD;
        RUNNINGTHREAD->pcfn = sleepfn;
    }
    else
    {
        /* Time to resume */
        RUNNINGTHREAD->interpctrl = INTERP_CTRL_RUN;
        RUNNINGTHREAD->pcfn = C_NULL;
        /* Return None */
        *tos = PM_NONE;
    }

    return PM_RET_OK;
}

PmReturn_t getbfn(pPmObj_t *tos)
{
    uint8_t b;
    pPmInt_t pb;
    PmReturn_t retval = PM_RET_OK;

    if (plat_isDataAvail())
    {
        /* Byte available, read it and resume */
        RUNNINGTHREAD->interpctrl = INTERP_CTRL_RUN;
        RUNNINGTHREAD->pcfn = C_NULL;

        retval = plat_getByte(&b);
        PM_RETURN_IF_ERROR(retval);

        retval = int_new((int32_t)b, &pb);
        *tos = (pPmObj_t)pb;
    }        
    else
    {
        /* Yield and continue to wait */
        RUNNINGTHREAD->interpctrl = INTERP_CTRL_CYIELD;
        RUNNINGTHREAD->pcfn = getbfn;
    }

    return retval;
}
"""

import profiler

maxint = 0x7FFFFFFF     # 2147483647

def sleep(n):
    profiler.set_flag(0, True)
    finish = time() + n
    if n > 10:
        # if we're going to be sitting around, run GC
        gcRun()
    _sleep_until(finish)
    profiler.set_flag(0, False)


def _sleep_until(n):
    """__NATIVE__
    uint32_t b, now;
    pPmObj_t pb;
    PmReturn_t retval = PM_RET_OK;

    pb = NATIVE_GET_LOCAL(0);

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(pb) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    b = ((pPmInt_t)pb)->val;
    
    do {
      plat_getMsTicks(&now);
    } while (now < b) ;

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass


def _modules():
    """__NATIVE__
    pPmObj_t pr = C_NULL;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return modules globals dict  on stack*/
    pr = (pPmObj_t)gVmGlobal.modules;
    NATIVE_SET_TOS(pr);

    return retval;
    """
    pass


def exit(val):
    """__NATIVE__
    pPmObj_t pval = C_NULL;
    PmReturn_t retval = PM_RET_OK;

    /* If no arg given, assume return 0 */
    if (NATIVE_GET_NUM_ARGS() == 0)
    {
        NATIVE_SET_TOS(PM_ZERO);
    }

    /* If 1 arg given, put it on stack */
    else if (NATIVE_GET_NUM_ARGS() == 1)
    {
        pval = NATIVE_GET_LOCAL(0);
        NATIVE_SET_TOS(pval);
    }

    /* If wrong number of args, raise TypeError */
    else
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Raise the SystemExit exception */
    PM_RAISE(retval, PM_RET_EX_EXIT);
    return retval;
    """
    pass


#
# Get a byte from the platform's default I/O
# Returns the byte in the LSB of the returned integer
#
def getb():
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Run the continuation function immediately */
    RUNNINGTHREAD->interpctrl = INTERP_CTRL_CCONT;
    RUNNINGTHREAD->pcfn = getbfn;

    /* Push dummy return value onto the top of the stack */
    NATIVE_SET_TOS(PM_NONE);

    return retval;
    """
    pass


#
# Returns a tuple containing the amout of heap available and the maximum
#
def heap():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t pavail;
    pPmInt_t pmax;
    pPmTuple_t ptup;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Allocate a tuple to store the return values */
    retval = tuple_new(2, &ptup);
    PM_RETURN_IF_ERROR(retval);

    /* Get the maximum heap size */
    retval = int_new(PM_HEAP_SIZE, &pmax);
    PM_RETURN_IF_ERROR(retval);

    /* Allocate an int to hold the amount of heap available */
    retval = int_new(heap_getAvail() - sizeof(PmInt_t), &pavail);
    PM_RETURN_IF_ERROR(retval);

    /* Put the two heap values in the tuple */
    ptup->items[0] = (pPmObj_t) pavail;
    ptup->items[1] = (pPmObj_t) pmax;

    /* Return the tuple on the stack */
    NATIVE_SET_TOS((pPmObj_t)ptup);

    return retval;
    """
    pass

#
# Print the free list
#
def printFreeList():
    """__NATIVE__
    heap_gcPrintFreelist();
    NATIVE_SET_TOS(PM_NONE);
    return PM_RET_OK;
    """
    pass

#
# Run the garbage collector
#
def gcRun():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    retval = heap_gcRun();
    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass    

#
# Sends the LSB of the integer out the platform's default I/O
#
def putb(b):
    """__NATIVE__
    uint8_t b;
    pPmObj_t pb;
    PmReturn_t retval = PM_RET_OK;

    pb = NATIVE_GET_LOCAL(0);

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(pb) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    b = ((pPmInt_t)pb)->val & 0xFF;
    if (-1 == lib_printf("%c", b))
    {
        PM_RAISE(retval, PM_RET_EX_IO);
        return retval;
    }
    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass


#
# Returns the number of milliseconds since the PyMite VM was initialized
#
def time():
    """__NATIVE__
    uint32_t t;
    pPmInt_t pt;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the system time (milliseconds since init) */
    retval = plat_getMsTicks(&t);
    PM_RETURN_IF_ERROR(retval);

    /*
     * Raise ValueError if there is an overflow
     * (plat_getMsTicks is unsigned; int is signed)
     */
    if ((int32_t)t < 0)
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* Return an int object with the time value */
    retval = int_new((int32_t)t, &pt);
    NATIVE_SET_TOS((pPmObj_t)pt);
    return retval;
    """
    pass


# :mode=c:
