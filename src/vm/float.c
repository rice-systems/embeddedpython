/* vm/float.c
 *
 * This file is Copyright 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x17


/**
 * \file
 * \brief Float Object Type
 *
 * Float object type operations.
 */


#include <math.h>
#include "pm.h"


#ifdef HAVE_FLOAT


PmReturn_t
float_new(float f, pPmObj_t *r_pf)
{
    PmReturn_t retval = PM_RET_OK;

    retval = heap_getChunk(sizeof(PmFloat_t), (uint8_t **)r_pf);
    PM_RETURN_IF_ERROR(retval);
    OBJ_SET_TYPE(*r_pf, OBJ_TYPE_FLT);
    ((pPmFloat_t) * r_pf)->val = f;
    return retval;
}


PmReturn_t
float_fromObj(pPmObj_t pf, pPmObj_t *r_pf)
{
    char const *pc;
    float n;
    int16_t length, digit;
    PmReturn_t retval = PM_RET_OK;
    bool negative = false;
    bool seen_decimal = false;
    float post_scale = 1.0;

    // if pf is null, return a zero
    if (pf) {
        switch (OBJ_GET_TYPE(pf)) {
            case OBJ_TYPE_FLT:    
                n = ((pPmFloat_t)pf)->val;
                break;
            case OBJ_TYPE_INT:
                n = ((pPmInt_t)pf)->val;
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
                while (length) 
                {
                    if (isspace(*pc)) 
                    {
                        pc++;
                        length--;
                    }
                    else
                    {
                        break;
                    }
                }

                if (*pc == '-') {
                    negative = true;
                    pc++;
                    length--;
                }

                // fetch any valid data herein
                while (length) 
                {
                    // determine if we're a valid character later
                    if ((*pc >= '0') && (*pc <= '9')) 
                    {
                        // scale from the last time, must start with zero
                        n *= 10;

                        digit = *pc - '0';
                        n += digit;
                        
                        if (seen_decimal) {
                            post_scale *= 10;
                        }
                    } 
                    else if ((*pc == '.') && (!seen_decimal))
                    {
                        seen_decimal = true;
                    }
                    else if (isspace(*pc)) 
                    {
                        // scrub off any trailing whitespace outside of this.
                        break;
                    }
                    else
                    {
                        // invalid in ANY base
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "invalid literal in string");
                        return retval;
                    }

                    length--;
                    pc++;
                }

                // scrub off any trailing whitespace
                while (length) {
                    if (isspace(*pc)) 
                    {
                        pc++;
                        length--;
                    }
                    else 
                    {
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "invalid literal in string");
                        return retval;
                    }
                }
                if (negative)
                {
                    n *= -1;
                }

                n /= post_scale;

                break;
            default:
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, 
                    "function takes one or fewer arguments");
                return retval;
        }
    } else {
        n = 0;
    }

    /* turn n into a Python float */
    retval = float_new(n, r_pf);
    return retval;
}

#ifdef HAVE_PRINT
PmReturn_t
float_print(pPmObj_t pf)
{
    PmReturn_t retval = PM_RET_OK;

    C_ASSERT(pf != C_NULL);

    /* Raise TypeError if obj is not a flt */
    if (OBJ_GET_TYPE(pf) != OBJ_TYPE_FLT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    lib_printf("%f", ((pPmFloat_t)pf)->val);
    return retval;
}
#endif /* HAVE_PRINT */


PmReturn_t
float_negative(pPmObj_t pf, pPmObj_t *r_pf)
{
    /* Create new int obj */
    return float_new(-((pPmFloat_t) pf)->val, r_pf);
}


PmReturn_t
float_op(pPmObj_t px, pPmObj_t py, pPmObj_t *r_pn, int8_t op)
{
    float x;
    float y;
    float r;
    PmReturn_t retval;

    /* Raise TypeError if args aren't ints or floats */
    if (((OBJ_GET_TYPE(px) != OBJ_TYPE_INT)
         && (OBJ_GET_TYPE(px) != OBJ_TYPE_FLT))
        || ((OBJ_GET_TYPE(py) != OBJ_TYPE_INT)
            && (OBJ_GET_TYPE(py) != OBJ_TYPE_FLT)))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the values as floats */
    if (OBJ_GET_TYPE(px) == OBJ_TYPE_INT)
    {
        x = (float)((pPmInt_t)px)->val;
    }
    else
    {
        x = ((pPmFloat_t) px)->val;
    }

    if (OBJ_GET_TYPE(py) == OBJ_TYPE_INT)
    {
        y = (float)((pPmInt_t)py)->val;
    }
    else
    {
        y = ((pPmFloat_t) py)->val;
    }

    /* Raise ZeroDivisionError if denominator is zero */
    if ((y == 0.0) && ((op == '/') || (op == '%')))
    {
        PM_RAISE(retval, PM_RET_EX_ZDIV);
    }

    /* Calculate x raised to y */
    switch (op)
    {
        /* *INDENT-OFF* */
        case '+': r = x + y; break;
        case '-': r = x - y; break;
        case '*': r = x * y; break;
        case '/': r = x / y; break;
        case '%': r = fmodf(x, y); break;
        case 'P': r = powf(x, y); break;
        default: r = 0.0; break;
        /* *INDENT-ON* */
    }

    retval = float_new(r, r_pn);

    return retval;
}

int8_t
float_compare(pPmObj_t pobj1, pPmObj_t pobj2)
{
    float a;
    float b;

    /* Raise TypeError if args aren't floats, bools, ints */
    if ( (OBJ_GET_TYPE(pobj1) != OBJ_TYPE_INT
           && OBJ_GET_TYPE(pobj1) != OBJ_TYPE_FLT
           && OBJ_GET_TYPE(pobj1) != OBJ_TYPE_BOL)
        || (OBJ_GET_TYPE(pobj2) != OBJ_TYPE_INT
           && OBJ_GET_TYPE(pobj2) != OBJ_TYPE_FLT
           && OBJ_GET_TYPE(pobj2) != OBJ_TYPE_BOL)
        )
    {
        return C_CMP_ERR;
    }

    /* Get the value of b as float */
    if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_INT)
    {
        b = (float)((pPmInt_t)pobj1)->val;
    }
    else if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_BOL)
    {
        if (((pPmBoolean_t)pobj1)->val == C_FALSE)
        {
            b = 0.0;
        }
        else
        {
            b = 1.0;
        }
    }
    else
    {
        b = ((pPmFloat_t) pobj1)->val;
    }

    /* Get the value of a as float */
    if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_INT)
    {
        a = (float)((pPmInt_t)pobj2)->val;
    }
    else if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_BOL)
    {
        if (((pPmBoolean_t)pobj2)->val == C_FALSE)
        {
            a = 0.0;
        }
        else
        {
            a = 1.0;
        }
    }
    else
    {
        a = ((pPmFloat_t) pobj2)->val;
    }
    
    /* Determine return value (Compare a and b) */
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

/*
 * Given an object of a numeric type (OBJ_TYPE_FLT, OBJ_TYPE_INT, or 
 * OBJ_TYPE_BOL) returns a float representation of that object's value.
 * Raises a TypeError if the object passed in was not of numeric type.
 */
PmReturn_t
float_getval(pPmObj_t num, pPmObj_t *val) {

    PmReturn_t retval = PM_RET_OK;
    float f;

    switch (OBJ_GET_TYPE(num)) {
        case OBJ_TYPE_FLT:    
            f = ((pPmFloat_t)num)->val;
            break;

        case OBJ_TYPE_INT:
            f = ((pPmInt_t)num)->val;
            break;

        case OBJ_TYPE_BOL:
            f = (num == PM_TRUE) ? 1 : 0;
            break;

        default:
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
    }

    retval = float_new(f, val);
    PM_RETURN_IF_ERROR(retval);
    return retval;
}

#endif /* HAVE_FLOAT */
