/* vm/int.c
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x08


/**
 * \file
 * \brief Integer Object Type
 *
 * Integer object type operations.
 */

#include <stdint.h>
#include <limits.h>

#include "pm.h"


PmReturn_t
int_new(int32_t n, pPmInt_t *r_pint)
{
    PmReturn_t retval = PM_RET_OK;

    /* If n is 0,1,-1, return static int objects from global struct */
    if (n == 0)
    {
        *r_pint = (pPmInt_t) PM_ZERO;
        return PM_RET_OK;
    }
    if (n == 1)
    {
        *r_pint = (pPmInt_t) PM_ONE;
        return PM_RET_OK;
    }
    if (n == -1)
    {
        *r_pint = (pPmInt_t) PM_NEGONE;
        return PM_RET_OK;
    }

    /* Else create and return new int obj */
    retval = heap_getChunk(sizeof(PmInt_t), (uint8_t **)r_pint);
    PM_RETURN_IF_ERROR(retval);
    OBJ_SET_TYPE(*r_pint, OBJ_TYPE_INT);
    (*r_pint)->val = n;
    return retval;
}

PmReturn_t
int_fromObj(pPmObj_t pf, pPmInt_t *pn, int16_t base)
{
    char const *pc;
    int32_t n;
    int16_t length, digit;
    PmReturn_t retval = PM_RET_OK;
    bool negative = false;
    
    // if pf is null, return a zero
    if (pf) {
        switch (OBJ_GET_TYPE(pf)) {
#ifdef HAVE_FLOAT
            case OBJ_TYPE_FLT:    
                n = ((pPmFloat_t)pf)->val;
                break;
#endif
            case OBJ_TYPE_INT:
                n = ((pPmInt_t)pf)->val;
                break;
            case OBJ_TYPE_BOL:
                n = (((pPmBoolean_t)pf) == (pPmBoolean_t)PM_TRUE);
                break;
            case OBJ_TYPE_STR:
                pc = (char const *)&(((pPmString_t)pf)->val);
                length = ((pPmString_t)pf)->length;

                if (length == 0) {
                    PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "cannot convert empty string");
                    return retval;
                }

                n = 0;

                // scrub off any leading whitespace
                while (length) {
                    if (isspace(*pc)) {
                        pc++;
                        length--;
                    } else {
                        break;
                    }
                }

                if (*pc == '-') {
                    negative = true;
                    pc++;
                    length--;
                }

                // fetch any valid data herein
                while (length) {
                    // determine if we're a valid character later
                    if ((*pc >= '0') && (*pc <= '9')) 
                    {
                        digit = *pc - '0';
                    } 
                    else if ((*pc >= 'a') && (*pc <= 'z')) 
                    {
                        digit = *pc - 'a' + 10;
                    } 
                    else if ((*pc >= 'A') && (*pc <= 'Z')) 
                    {
                        digit = *pc - 'A' + 10;
                    } 
                    else if (isspace(*pc))
                    {
                        break;
                    }
                    else
                    {
                        // invalid in ANY base
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "invalid literal in string");
                        return retval;
                    }

                    if (digit >= base) {
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, 
                            "invalid literal in string for given base");
                        return retval;
                    }

                    // scale from the last time, must start with zero
                    n *= base;
                    n += digit;
                    length--;
                    pc++;
                }

                // scrub off any trailing whitespace
                while (length) {
                    if (isspace(*pc)) {
                        pc++;
                        length--;
                    } else {
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "invalid literal in string");
                        return retval;
                    }
                }

                if (negative) {
                    n *= -1;
                }

                break;
            default:
                PM_RAISE(retval, PM_RET_EX_TYPE);
                return retval;
        }
    } else {
        n = 0;
    }

    /* turn n into a Python int */
    retval = int_new(n, pn);
    return retval;
}

PmReturn_t
int_positive(pPmInt_t pobj, pPmInt_t *r_pint)
{
    PmReturn_t retval;

    /* Raise TypeError if obj is not an int */
    if (OBJ_GET_TYPE(pobj) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* RIXNER: this is stupid, integers are immutable, so the new one
     * should just point to the same object as the original.
     */

    /* Create new int obj */
    return int_new(pobj->val, r_pint);
}


PmReturn_t
int_negative(pPmInt_t pobj, pPmInt_t *r_pint)
{
    PmReturn_t retval;

    /* Raise TypeError if obj is not an int */
    if (OBJ_GET_TYPE(pobj) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Create new int obj */
    return int_new(-pobj->val, r_pint);
}


PmReturn_t
int_bitInvert(pPmInt_t pobj, pPmInt_t *r_pint)
{
    PmReturn_t retval;

    /* Raise TypeError if obj is not an int */
    if (OBJ_GET_TYPE(pobj) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Create new int obj */
    return int_new(~pobj->val, r_pint);
}

#ifdef HAVE_PRINT
PmReturn_t
int_print(pPmInt_t pint)
{
    PmReturn_t retval = PM_RET_OK;

    C_ASSERT(pint != C_NULL);

    /* Raise TypeError if obj is not an int */
    if (OBJ_GET_TYPE(pint) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    lib_printf("%d", (int32_t) pint->val);

    return retval;
}
#endif /* HAVE_PRINT */


PmReturn_t
int_pow(pPmInt_t px, pPmInt_t py, pPmInt_t *r_pn)
{
    int32_t x;
    int32_t y;
    int32_t n;
    PmReturn_t retval;

    /* Raise TypeError if args aren't ints */
    if ((OBJ_GET_TYPE(px) != OBJ_TYPE_INT)
        || (OBJ_GET_TYPE(py) != OBJ_TYPE_INT))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    x = px->val;
    y = py->val;

    /* Raise Value error if exponent is negative */
    if (y < 0)
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* Calculate x raised to y */
    n = 1;
    while (y > 0)
    {
        n = n * x;
        y--;
    }
    retval = int_new(n, r_pn);

    return retval;
}

int8_t
int_compare(pPmObj_t pobj1, pPmObj_t pobj2)
{
    int32_t a;
    int32_t b;

    /* Set b based off of pobj1 */
    if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_INT)
    {
        b = ((pPmInt_t)pobj1)->val;
    }
    else if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_BOL)
    {
        if (((pPmBoolean_t)pobj1)->val == C_FALSE)
        {
            b = 0;
        }
        else
        {
            b = 1;
        }
    }
    else
    {
        C_ASSERT(0); //raise an error; should not occur, pobj1 should be int or bool.
    }

    /* Set a based off of pobj2 */
    if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_INT)
    {
        a = ((pPmInt_t)pobj2)->val;
    }
    else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_BOL)
    {
        if (((pPmBoolean_t)pobj2)->val == C_FALSE)
        {
            a = 0;
        }
        else
        {
            a = 1;
        }
    }
    else
    {
        C_ASSERT(0); //raise an error; should not occur, pobj2 should be int or bool.
    }

    /* Compare a and b */ 
    if (a > b)
    {
        return C_GT; //1; pobj2(a) > pobj1(b)
    }
    else if (a == b)
    {
        return C_EQ; //0; pobj2(a) == pobj1(b)
    }
    else
    {
        return C_LT; //-1; pobj2(a) < pobj1(b)
    }

}
