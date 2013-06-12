/* vm/tuple.c
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
#define __FILE_ID__ 0x13


/**
 * \file
 * \brief Tuple Object Type
 *
 * Tuple object type operations.
 */


#include "pm.h"


/* The follwing value should match that in pmImgCreator.py */
#define MAX_TUPLE_LEN 253

PmReturn_t
tuple_new(uint16_t n, pPmTuple_t *r_ptuple)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t size = 0;

    /* Raise a SystemError for a Tuple that is too large */
    if (n > MAX_TUPLE_LEN)
    {
        PM_RAISE(retval, PM_RET_EX_SYS);
        return retval;
    }

    /* Calc size of struct to hold tuple; (n-1) because PmTuple_t has val[1] */
    size = sizeof(PmTuple_t) + ((n - 1) * sizeof(pPmObj_t));

    /* Allocate a tuple */
    retval = heap_getChunk(size, (uint8_t **)r_ptuple);
    PM_RETURN_IF_ERROR(retval);
    OBJ_SET_TYPE(*r_ptuple, OBJ_TYPE_TUP);

    /* Set the number of objs in the tuple */
    (*r_ptuple)->length = n;

    /* No need to null the ptrs because they are set by the caller */
    return retval;
}

PmReturn_t
tuple_copy(pPmTuple_t ptup, pPmTuple_t *r_ptup)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t len, i;
    pPmObj_t r_pobj1;
        //r_pobj2;
    
    len = tuple_getLength(ptup);
    
    retval = tuple_new(len, r_ptup);
    PM_RETURN_IF_ERROR(retval);
    FP->liveObj = (pPmObj_t)*r_ptup;

    for (i = 0; i < len; i++)
    {
        retval = tuple_getItem(ptup, i, &r_pobj1);
        PM_RETURN_IF_ERROR_SET_NULL(retval);
        //retval = obj_copy(r_pobj1, &r_pobj2);
        //PM_RETURN_IF_ERROR_SET_NULL(retval);
        (*r_ptup)->items[i] = r_pobj1;//2;
    }

    FP->liveObj = C_NULL;
    return retval;
}

PmReturn_t
tuple_replicate(pPmTuple_t ptup, int16_t n, pPmObj_t *r_ptuple)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t length;
    int16_t i;
    int16_t j;
    pPmPackTuple_t r_ptp;
    pPmTuple_t r_ptup;

    /* Raise TypeError if object is not a Tuple */
    if ((OBJ_GET_TYPE(ptup) != OBJ_TYPE_TUP) && (OBJ_GET_TYPE(ptup) != OBJ_TYPE_PTP))
    {
        PM_RAISE(retval, PM_RET_EX_SYS);
        return retval;
    }

    C_ASSERT(n >= 0);

    if (OBJ_GET_TYPE(ptup) == OBJ_TYPE_PTP)
    {
        retval = packtuple_replicate((pPmPackTuple_t)ptup, n, &r_ptp);
        PM_RETURN_IF_ERROR(retval);
        *r_ptuple = (pPmObj_t)r_ptp;
    }

    else
    {
        /* Allocate the new tuple */
        length = ptup->length;
        retval = tuple_new(length * n, &r_ptup);
        PM_RETURN_IF_ERROR(retval);

        /* Copy src tuple the designated number of times */
        for (i = 0; i < n; i++)
        {
            for (j = 0; j < length; j++)
            {
                (r_ptup)->items[length * i + j] = ptup->items[j];
            }
        }
        *r_ptuple = (pPmObj_t)r_ptup;
    }
    return retval;
}


PmReturn_t
tuple_getItem(pPmTuple_t ptup, int16_t index, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pobj;
    int16_t len = tuple_getLength(ptup);

    /* Adjust for negative index */
    if (index < 0)
    {
        index += len;
    }

    /* Raise IndexError if index is out of bounds */
    if ((index < 0) || (index >= len))
    {
        PM_RAISE(retval, PM_RET_EX_INDX);
        return retval;
    }

    if (OBJ_GET_TYPE((pPmObj_t)ptup) == OBJ_TYPE_TUP)
    {
        /* Get the tuple item */
        *r_pobj = ptup->items[index];
    }
    else // OBJ_TYPE_PTP
    {
        retval = packtuple_getItem((pPmPackTuple_t)ptup, index, &pobj);
        PM_RETURN_IF_ERROR(retval);
        *r_pobj = pobj;
    }

    return retval;
}

int16_t
tuple_getLength(pPmTuple_t ptup)
{
    if (OBJ_GET_TYPE((pPmObj_t)ptup) == OBJ_TYPE_TUP)
    {
        return ptup->length;
    }
    else // OBJ_TYPE_PTP
    {
        return ((pPmPackTuple_t)ptup)->length;
    }
} 

PmReturn_t
tuple_index(pPmTuple_t ptup, pPmObj_t pitem, int16_t *r_index)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pobj;
    int16_t length;
    int16_t index;

    /* If it's not a tuple or packed tuple, raise TypeError */
    if (!IS_TUPLE_OBJ(ptup))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    length = tuple_getLength(ptup);

    /* Iterate over the list's contents */
    for (index = 0; index < length; index++)
    {
        retval = tuple_getItem(ptup, index, &pobj);
        PM_RETURN_IF_ERROR(retval);

        /* If the list item matches the given item, return the index */
        if (obj_isEqual(pobj, pitem) == C_EQ)
        {
            *r_index = index;
            return PM_RET_OK;
        }
    }

    PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "object not found in tuple");
    return retval;
}


#ifdef HAVE_SLICING
PmReturn_t
tuple_slice(pPmTuple_t ptup1, int16_t start, int16_t end, pPmObj_t *r_ptuple)
{
    PmReturn_t retval = PM_RET_OK;
    pPmTuple_t ptup = C_NULL;
    uint16_t len;
    uint16_t i = 0;
    len = end - start;
    
    retval = tuple_new(len, &ptup);
    PM_RETURN_IF_ERROR(retval);

    while (len > 0) {
        ptup->items[i] = ptup1->items[start+i];
        i++;
        len--;
    }

    *r_ptuple = (pPmObj_t)ptup;
    return retval;
}
#endif /* HAVE_SLICING */
