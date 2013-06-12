# lib/math.py
#
# General purpose math functions.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

"""__NATIVE__
#include <math.h>
#include "pm.h"
"""

pi = 3.141592653589793
e  = 2.718281828459045

def sqrt(num):
    '''__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = sqrtf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    '''
    pass

def sin(num):
    """__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = sinf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    """
    pass

def cos(num):
    """__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = cosf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    """
    pass

def tan(num):
    """__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = tanf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    """
    pass

def asin(num):
    """__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = asinf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    """
    pass

def acos(num):
    """__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = acosf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    """
    pass

def atan(num):
    """__NATIVE__
    pPmObj_t   pobj;
    pPmObj_t   pf;
    float      f;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj = NATIVE_GET_LOCAL(0);
    retval = float_getval(pobj, &pf);
    PM_RETURN_IF_ERROR(retval);

    f = ((pPmFloat_t)pf)->val;
    f = atanf(f);
    retval = float_new(f, &pf);

    NATIVE_SET_TOS(pf);
    return retval;
    """
    pass

def atan2(y, x):
    """__NATIVE__
    pPmObj_t   pobj1;
    pPmObj_t   pobj2;
    pPmObj_t   pf1;
    pPmObj_t   pf2;
    float      f1, f2;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj1 = NATIVE_GET_LOCAL(0);
    pobj2 = NATIVE_GET_LOCAL(1);
    
    retval = float_getval(pobj1, &pf1);
    PM_RETURN_IF_ERROR(retval);
    f1 = ((pPmFloat_t)pf1)->val;

    retval = float_getval(pobj2, &pf2);
    PM_RETURN_IF_ERROR(retval);
    f2 = ((pPmFloat_t)pf2)->val;

    f1 = atan2f(f1, f2);
    retval = float_new(f1, &pf1);

    NATIVE_SET_TOS(pf1);
    return retval;
    """
    pass

def pow(x, y):
    """__NATIVE__
    pPmObj_t   pobj1;
    pPmObj_t   pobj2;
    pPmObj_t   pf1;
    pPmObj_t   pf2;
    float      f1, f2;
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pobj1 = NATIVE_GET_LOCAL(0);
    pobj2 = NATIVE_GET_LOCAL(1);

    retval = float_getval(pobj1, &pf1);
    PM_RETURN_IF_ERROR(retval);
    f1 = ((pPmFloat_t)pf1)->val;

    retval = float_getval(pobj2, &pf2);
    PM_RETURN_IF_ERROR(retval);
    f2 = ((pPmFloat_t)pf2)->val;

    f1 = powf(f1, f2);
    retval = float_new(f1, &pf1);

    NATIVE_SET_TOS(pf1);
    return retval;
    """
    pass

def radians(degrees):
    return float(degrees) * (pi / 180.0)

def degrees(radians):
    return float(radians) * (180.0 / pi)

def modf(num):
    inum = int(num)
    return (num - inum, float(inum))

def fabs(num):
    if num < 0:
        return -num
    return num

def hypot(x, y):
    return sqrt((x * x) + (y * y))

#:mode=c:
