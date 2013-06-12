/* vm/seq.c
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
#define __FILE_ID__ 0x14


/**
 * \file
 * \brief Sequence
 *
 * Functions that operate on sequences
 */


#include "pm.h"


/*
 * Compares two sequence objects
 * Assumes both objects are of same type (guaranteed by obj_isEqual)
 */
int8_t
seq_isEqual(pPmObj_t pobj1, pPmObj_t pobj2)
{
    int16_t l1;
    int16_t l2;
    pPmObj_t pa;
    pPmObj_t pb;
    PmReturn_t retval;
    int8_t retcompare;

    /* Get the lengths of supported types or return differ */
    if (IS_TUPLE_OBJ(pobj1) && IS_TUPLE_OBJ(pobj2))
    {
        // pobj1 (and pobj2) is a packed tuple or tuple
        l1 = tuple_getLength((pPmTuple_t)pobj1);
        l2 = tuple_getLength((pPmTuple_t)pobj2);
    }
    else if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_LST
             && OBJ_GET_TYPE(pobj2) == OBJ_TYPE_LST)
    {
        l1 = ((pPmList_t)pobj1)->length;
        l2 = ((pPmList_t)pobj2)->length;
    }
    else if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_SET
             && OBJ_GET_TYPE(pobj2) == OBJ_TYPE_SET)
    {
        return set_isEqual((pPmSet_t)pobj1, (pPmSet_t)pobj2);
    }
    else
    {
        return C_NEQ;
    }

    /* Return if the lengths differ */
    if (l1 != l2)
    {
        return C_NEQ;
    }

    /* Compare all items in the sequences */
    while (--l1 >= 0)
    {
        retval = seq_getItem(pobj1, l1, &pa);
        if (retval != PM_RET_OK)
        {
            return C_NEQ;
        }
        retval = seq_getItem(pobj2, l1, &pb);
        if (retval != PM_RET_OK)
        {
            return C_NEQ;
        }
        retcompare = obj_isEqual(pa, pb);
        if (retcompare != C_EQ)
        {
            return retcompare;
        }
    }

    return C_EQ;
}

int8_t
seq_compare(pPmObj_t pobj1, pPmObj_t pobj2, int8_t match, pPmObj_t punb_dict)
{   
    int16_t i=0;
    pPmObj_t pelement2; //from pobj2
    pPmObj_t pelement1; //from pobj1
    int16_t len2; //length of pobj2
    int16_t len1; //length of pobj1
    int8_t result;

    if ((OBJ_GET_TYPE(pobj1) != OBJ_GET_TYPE(pobj2)) &&
        (!(IS_TUPLE_OBJ(pobj1) && IS_TUPLE_OBJ(pobj2))))
    {
        return C_CMP_ERR;
    }

    seq_getLength(pobj2, &len2);
    seq_getLength(pobj1, &len1);

    while (len2 > i && len1 > i)
    {
        seq_getItem(pobj2, i, &pelement2);   
        seq_getItem(pobj1, i, &pelement1);

            /* called from obj_compare, match = false */
            result = obj_compare(pelement1, pelement2);
            if (result != C_EQ)
            {
                return result; // either GT or LT
            }
        i++;
    }
            
    if (len1 == i && len2 == i) //both obj1 and obj2 reached their length
    {
        return C_EQ; //0; obj2 == obj1
    }
    else if (len1 == i) //obj1 reached its length, but obj2 did not
    {
        return C_GT; //1; obj2 > obj1
    }
    else if (len2 == i)
    {
        return C_LT; //-1; obj2 < obj1
    }
    else //neither obj2 nor obj1 reached their length
    { //this should never be reached (handled in while loop)
        C_ASSERT(0);
    }

}

/* Returns the length of the sequence */
PmReturn_t
seq_getLength(pPmObj_t pobj, int16_t *r_index)
{
    PmReturn_t retval = PM_RET_OK;

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_STR:
            *r_index = ((pPmString_t)pobj)->length;
            break;

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
            *r_index = tuple_getLength((pPmTuple_t)pobj);
            break;

        case OBJ_TYPE_LST:
            *r_index = ((pPmList_t)pobj)->length;
            break;

        case OBJ_TYPE_XRA:
            *r_index = ((pPmXrange_t)pobj)->length;
            break;

        case OBJ_TYPE_DIC:
            *r_index = ((pPmDict_t)pobj)->length;
            break;

        case OBJ_TYPE_SET:
            *r_index = ((pPmSet_t)pobj)->length;
            break;

        default:
            /* Raise TypeError, non-sequence object */
            PM_RAISE(retval, PM_RET_EX_TYPE);
            break;
    }

    return retval;
}


/* Returns the object sequence[index] */
PmReturn_t
seq_getSubscript(pPmObj_t pobj, int16_t index, pPmObj_t *r_pobj)
{
    PmReturn_t retval;

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_STR:
        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_LST:
        case OBJ_TYPE_XRA:
            /* Subscriptable object */
            retval = seq_getItem(pobj, index, r_pobj);
            break;

        default:
            /* Raise TypeError, unsubscriptable object */
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "unsubscriptable item");
            break;
    }

    return retval;
}

PmReturn_t
seq_getItem(pPmObj_t pobj, int16_t index, pPmObj_t *r_pobj)
{
    PmReturn_t retval;
    uint8_t c;

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_STR:
            /* Adjust for negative index */
            if (index < 0)
            {
                index += ((pPmString_t)pobj)->length;
            }

            /* Raise IndexError if index is out of bounds */
            if ((index < 0) || (index >= ((pPmString_t)pobj)->length))
            {
                PM_RAISE(retval, PM_RET_EX_INDX);
                break;
            }

            /* Get the character from the string */
            c = ((pPmString_t)pobj)->val[index];

            /* Create a new string from the character */
            retval = string_new((char const *)&c, 1, (pPmString_t *)r_pobj);
            break;

        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
            /* Get the tuple item */
            retval = tuple_getItem((pPmTuple_t)pobj, index, r_pobj);
            break;

        case OBJ_TYPE_LST:
            /* Get the list item */
            retval = list_getItem((pPmList_t)pobj, index, r_pobj);
            break;

        case OBJ_TYPE_XRA:
            /* Get the list item */
            retval = xrange_getItem((pPmXrange_t)pobj, index, (pPmInt_t *)r_pobj);
            break;

        case OBJ_TYPE_SET:
            /* Get the set item */
            retval = set_getItem((pPmSet_t)pobj, index, r_pobj);
            break;

        default:
            /* Raise TypeError, non-sequence object */
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "non-sequence object");
            break;
    }

    return retval;
}


PmReturn_t
seqiter_getNext(pPmObj_t pobj, pPmObj_t *r_pitem)
{
    PmReturn_t retval;
    int16_t length;

    C_ASSERT(pobj != C_NULL);
    C_ASSERT(*r_pitem != C_NULL);
    C_ASSERT(OBJ_GET_TYPE(pobj) == OBJ_TYPE_SQI);

    /*
     * Raise TypeError if sequence iterator's object is not a sequence
     * otherwise, the get sequence's length
     */
    retval = seq_getLength(((pPmSeqIter_t)pobj)->si_sequence, &length);
    PM_RETURN_IF_ERROR(retval);

    /* Raise StopIteration if at the end of the sequence */
    if (((pPmSeqIter_t)pobj)->si_index == length)
    {
        /* Make null the pointer to the sequence */
        ((pPmSeqIter_t)pobj)->si_sequence = C_NULL;
        PM_RAISE(retval, PM_RET_EX_STOP);
        return retval;
    }

    /* Get the item at the current index */
    retval = seq_getItem(((pPmSeqIter_t)pobj)->si_sequence,
                         ((pPmSeqIter_t)pobj)->si_index, r_pitem);

    /* Increment the index */
    ((pPmSeqIter_t)pobj)->si_index++;

    return retval;
}


PmReturn_t
seqiter_new(pPmObj_t pobj, pPmObj_t *r_pobj)
{
    PmReturn_t retval;
    uint8_t *pchunk;
    pPmSeqIter_t psi;

    C_ASSERT(pobj != C_NULL);
    C_ASSERT(*r_pobj != C_NULL);

    /* Raise a TypeError if pobj is not a sequence */
    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_STR:
        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_XRA:
        case OBJ_TYPE_LST:
        case OBJ_TYPE_SET:
            /* Sequence type */
            break;

        default:
            /* Non-sequence type */
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected sequence");
            return retval;
    }

    /* Alloc a chunk for the sequence iterator obj */
    retval = heap_getChunk(sizeof(PmSeqIter_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);

    /* Set the sequence iterator's fields */
    psi = (pPmSeqIter_t)pchunk;
    OBJ_SET_TYPE(psi, OBJ_TYPE_SQI);
    psi->si_sequence = pobj;
    psi->si_index = 0;

    *r_pobj = (pPmObj_t)psi;
    return retval;
}

#ifdef HAVE_PRINT
PmReturn_t
seq_print(pPmObj_t pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t   pitem;
    int16_t    index;
    int16_t    length;
    char      *openbracket, *closebracket;

    C_ASSERT(pobj != C_NULL);

    switch (OBJ_GET_TYPE(pobj))
    {
        case OBJ_TYPE_TUP:
        case OBJ_TYPE_PTP:
            openbracket = "(";
            closebracket = ")";
            break;

        case OBJ_TYPE_LST:
            openbracket = "[";
            closebracket = "]";
            break;

        case OBJ_TYPE_SET:
            openbracket = "set([";
            closebracket = "])";
            break;

        default:
            /* Raise TypeError, not printable sequence */
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
    }

    if (-1 == lib_printf("%s", openbracket))
    {
        PM_RAISE(retval, PM_RET_EX_IO);
        return retval;
    }

    /* Iterate over the sequence */
    retval = seq_getLength(pobj, &length);
    PM_RETURN_IF_ERROR(retval);
    for (index = 0; index < length; index++)
    {
        if (index != 0)
        {
            if (-1 == lib_printf(", "))
            {
                PM_RAISE(retval, PM_RET_EX_IO);
                return retval;
            }
        }

        /* Print each item */
        retval = seq_getItem(pobj, index, &pitem);
        PM_RETURN_IF_ERROR(retval);
        retval = obj_print(pitem, 1);
        PM_RETURN_IF_ERROR(retval);
    }

    if (-1 == lib_printf("%s", closebracket))
    {
        PM_RAISE(retval, PM_RET_EX_IO);
        return retval;
    }

    return retval;
}
#endif /* HAVE_PRINT */

#ifdef HAVE_SLICING
PmReturn_t
seq_slice(pPmObj_t pobj, int16_t start, int16_t end, bool to_end, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t len;

    // fetch the appropriate type
    if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_STR) {
        len = ((pPmString_t) pobj)->length;
    } else if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_TUP) {
        len = ((pPmTuple_t) pobj)->length;
    } else if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_LST) {
        len = ((pPmList_t) pobj)->length;
    } else {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    if (to_end) {
        end = len;
    }

    if (end > len) {
        end = len;
    }
    
    if (start > len) {
        start = len;
    }

    if (start < 0) {
        start = len+start;

        if (start < 0) {
            start = 0;
        }
    }

    if (end < 0) {
        end = len+end;

        if (end < 0) {
            end = 0;
        }
    }

    if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_STR) {
        retval = string_slice((pPmString_t) pobj, start, end, r_pobj);
    } else if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_TUP) {
        retval = tuple_slice((pPmTuple_t) pobj, start, end, r_pobj);
    } else if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_LST) {
        retval = list_slice((pPmList_t) pobj, start, end, r_pobj);
    }

    return retval;
}
#endif /* HAVE_SLICING */

