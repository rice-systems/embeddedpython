/* vm/packtuple.c
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x1D


/**
 * \file
 * \brief Packed Tuple Object Type
 *
 * Packed Tuple object type operations.
 */


#include "pm.h"

PmReturn_t
packtuple_packSetup(pPmTuple_t ptup, pPmPackTuple_t *r_pptp)
{
    PmReturn_t retval = PM_RET_OK;
    int8_t r_bol;
    pPmObj_t r_pobj;
        
    /* Raise TypeError if ptup is not a tuple */
    if (OBJ_GET_TYPE(ptup) != OBJ_TYPE_TUP)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "cannot pack an object that is not a tuple");
        return retval;
    }

    retval = obj_isPackable((pPmObj_t)ptup, &r_bol, &r_pobj);
    PM_RETURN_IF_ERROR(retval);
    /* Raise a TypeError if ptup contains an object not able to be packed */
    if (r_bol == C_FALSE)
    {
        PM_RAISE_WITH_INFO_AND_OBJ(retval, PM_RET_EX_TYPE, "cannot pack a tuple containing: ", r_pobj);
        return retval;
    } 

    // pack the objects into the new packed tuple
    retval = packtuple_pack(ptup, r_pptp);
    PM_RETURN_IF_ERROR(retval);

    return retval;

}

PmReturn_t
packtuple_pack(pPmTuple_t ptup, pPmPackTuple_t *r_pptp)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t objsize = 0;
    pPmPackTuple_t pptp;
    uint8_t *pchunk;
    uint8_t *pdst;

    // the pack tuple setup guarantees ptup is a tuple

    /* Allocate the space for new packed tuple */
    // get the size of everything inside the tuple
    retval = packtuple_getSize((pPmObj_t)ptup, &objsize);
    PM_RETURN_IF_ERROR(retval);
    //lib_printf("size in pack %d \n", sizeof(PmPackTuple_t) + objsize);

    // get the space for the new packed tuple
    retval = heap_getChunk(sizeof(PmPackTuple_t) + objsize, &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pptp = (pPmPackTuple_t)pchunk;

    /* Fill the packed tuple object */
    // set the type and fields of the packed tuple
    OBJ_SET_TYPE(pptp, OBJ_TYPE_PTP);
    pptp->size = objsize;
    pptp->length = ptup->length;
    pdst = (uint8_t *)&(pptp->array[0]);

    // pack the objects into the new packed tuple
    retval = packtuple_packcopy(pdst, ptup);
    PM_RETURN_IF_ERROR(retval);

    *r_pptp = pptp;
    return retval;
}

PmReturn_t
packtuple_packcopy(uint8_t *pdst, pPmTuple_t ptup)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pobj;
    int16_t i, objsize;
    uint8_t *psrc;
    pPmPackTuple_t r_pptp;
    
    for (i = 0; i < ptup->length; i++)
    {
        retval = tuple_getItem(ptup, i, &pobj);
        /* obj_getSize runs through first getting sizes, and guarantees there are nothing but tuples
           and acceptable objects for packing */
        if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_TUP)
        {
            // create a new packed tuple (which calls packtuple_copy)
            retval = packtuple_pack((pPmTuple_t)pobj, &r_pptp);
            PM_RETURN_IF_ERROR(retval);
            // copy the new packed tuple into the already allocated space
            psrc = (uint8_t *)r_pptp;
            memcpy(pdst, (const uint8_t *) psrc, OBJ_GET_SIZE(r_pptp));
            pdst += OBJ_GET_SIZE(r_pptp);
        }
        else 
        {
            /* pobj is not a sequence or it is an already packed tuple */
            objsize = OBJ_GET_SIZE(pobj);
            psrc = (uint8_t *)pobj;
            memcpy(pdst, (const uint8_t *) psrc, objsize);
            pdst += objsize;
        }
    }
    
    return retval;
}

PmReturn_t
packtuple_getSize(pPmObj_t pobj, uint16_t *size)
{
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pobj2;
    int16_t i;
    
    /* packtuple_pack guarantees the first object is a tuple */
    for (i = 0; i < ((pPmTuple_t)pobj)->length; i++)
    {
        retval = tuple_getItem((pPmTuple_t)pobj, i, &pobj2);
        /* already checked and no non-allowed types are inside of the tuple */
        if (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_TUP)
        {
            *size += sizeof(PmPackTuple_t); // it's a tuple, but will become a packed tuple
            retval = packtuple_getSize(pobj2, size);
            PM_RETURN_IF_ERROR(retval);
        }
        else 
        {
            /* pobj2 is not a sequence or it is an already packed tuple */
            *size += OBJ_GET_SIZE(pobj2);
        }
    }
    
    return retval;
}

PmReturn_t
packtuple_replicate(pPmPackTuple_t pptp, int16_t n, pPmPackTuple_t *r_pptp)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i;
    uint16_t size;
    uint8_t *pchunk;
    uint8_t *pdst = C_NULL;
    uint8_t *psrc; 
    pPmPackTuple_t pptup;

    /* Raise TypeError if object is not a Packed Tuple */
    if (OBJ_GET_TYPE(pptp) != OBJ_TYPE_PTP)
    {
        PM_RAISE(retval, PM_RET_EX_SYS);
        return retval;
    }

    C_ASSERT(n >= 0);

    /* Allocate the space for new packed tuple */
    size = pptp->size;
    retval = heap_getChunk(sizeof(PmPackTuple_t) + (size * n), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pptup = (pPmPackTuple_t)pchunk;

    /* Fill the packed tuple object */
    OBJ_SET_TYPE(pptup, OBJ_TYPE_PTP);
    pptup->size = (pptp->size * n);
    pptup->length = (pptp->length *n);
    
    psrc = (uint8_t *)pptp->array;
    pdst = (uint8_t *)&(pptup->array[0]);
    for (i = 0; i < n; i++)
    {
        memcpy(pdst, psrc, pptp->size);
        pdst += pptp->size;
    }

    *r_pptp = pptup;
    return retval;
}

PmReturn_t
packtuple_getItem(pPmPackTuple_t pptup, int16_t index, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i;
    pPmObj_t obj;
    uint8_t * array = pptup->array;
    
    /* Adjust for negative index */
    if (index < 0)
    {
        index += pptup->length;
    }

    /* Raise IndexError if index is out of bounds */
    if ((index < 0) || (index >= pptup->length))
    {
        PM_RAISE(retval, PM_RET_EX_INDX);
        return retval;
    }

    /* Get the packed tuple item */
    for (i = 0; i <= index; i++)
    {
        //find the size of the first object in the packed tuple
        obj = (pPmObj_t)(array); // get the obj
        C_ASSERT((uint8_t *)obj < (array + pptup->size));
        array += OBJ_GET_SIZE(obj); // get the length of the size in bytes (in the array)        
    }

        if (heap_addrInHeap((uint8_t *)obj))
        {
            /* if the object is in the heap, make a copy */
            retval = obj_copy(obj, r_pobj);
        }
        else
        {
            /* the object is in flash, return the object */
            *r_pobj = obj;
        }

    return retval;
}


#ifdef HAVE_SLICING
PmReturn_t
packtuple_slice(pPmPackTuple_t pptp, int16_t start, int16_t end, pPmObj_t *r_pptp)
{
    PmReturn_t retval = PM_RET_OK;

    return retval;
}
#endif /* HAVE_SLICING */
