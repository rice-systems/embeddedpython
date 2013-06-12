# lib/profiler.py
#
# Controls and processes data for the various system profilers.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys

def profile_function(f, frequency=100):
    reset()
    start(frequency)
    f()
    stop()
    vmstats()

def start(frequency=2001):
    _set_frequency(frequency)
    _start()

# this probably should do some bounds checking
# on flag...
def set_flag(flag, value):
    if value:
        int_value = 1
    else:
        int_value = 0

    _set_flag(flag, int_value)

def _set_flag(flag, value):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    int flag;
    int value;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    flag = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    value = ((pPmInt_t)p1)->val;

#ifdef HAVE_PROFILER
    if (value==1) {
        gVmGlobal.profiler_flags[flag] = true;
    } else {
        gVmGlobal.profiler_flags[flag] = false;
    }
#endif

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

def _set_frequency(frequency):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    int frequency;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    frequency = ((pPmInt_t)p0)->val;

#ifdef HAVE_PROFILER
    retval = plat_setProfilerFrequency(frequency);
    gVmGlobal.profiler_frequency = frequency;
#endif

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

def _start():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    profiler_startstop(1);
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass
    
def stop():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    profiler_startstop(0);
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass
    
def reset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    retval = profiler_init();
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass
    
def vmstats():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    profiler_vmstats();
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def pystats():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    profiler_pystats();
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def callstats():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    profiler_callstats();
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def set_context():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    retval = profiler_set_context();
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def _sample():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

#ifdef HAVE_PROFILER
    profiler_tick();
#endif

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

DICT_PHASES = {0:"(other)", 1:"LOAD_ATTR", 2:"BINARY_SUBSCR", 3:"LOAD_GLOBAL"}

def dict_profile():
    profiles = _dict_profile()

    print "-start-"

    for (n, (lookups, hits, entries_walked, entries_total)) in enumerate(profiles):
        print DICT_PHASES[n]
        if lookups:
            print "lookups: ", lookups
            print "hit rate: ", float(hits) / float(lookups)
            print "avg entries searched: ", float(entries_walked) / float(lookups)
            print "avg entries total: ", float(entries_total) / float(lookups)
        else:
            print "(no lookups)"
        print ""

    print "-end-"

def _dict_profile():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmList_t pl = (pPmList_t) PM_NONE;

#ifdef HAVE_PROFILER
    retval = profiler_dictstats(&pl);
    PM_RETURN_IF_ERROR(retval);
#endif

    NATIVE_SET_TOS((pPmObj_t) pl);
    return retval;
    '''
    pass
