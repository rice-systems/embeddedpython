/* vm/dict.c
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
#define __FILE_ID__ 0x02


/**
 * \file
 * \brief Dict Object Type
 *
 * Dict object type operations.
 */


#include "pm.h"


PmReturn_t
dict_new(pPmDict_t *r_pdict)
{
    PmReturn_t retval = PM_RET_OK;
    pPmDict_t pdict = C_NULL;
    uint8_t *pchunk;
    
    /* Allocate a dict */
    retval = heap_getChunk(sizeof(PmDict_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);

    /* Init dict fields */
    pdict = (pPmDict_t)pchunk;
    OBJ_SET_TYPE(pdict, OBJ_TYPE_DIC);
    pdict->length = 0;
    pdict->d_keys = C_NULL;
    pdict->d_vals = C_NULL;

    *r_pdict = pdict;
    return retval;
}


PmReturn_t
dict_clear(pPmDict_t pdict)
{
    PmReturn_t retval = PM_RET_OK;

    C_ASSERT(pdict != C_NULL);

    /* Raise TypeError if arg is not a dict */
    if (OBJ_GET_TYPE(pdict) != OBJ_TYPE_DIC)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* clear length */
    pdict->length = 0;

    /* Free the keys and values seglists if needed */
    if (pdict->d_keys != C_NULL)
    {
        PM_RETURN_IF_ERROR(seglist_clear(pdict->d_keys));
        PM_RETURN_IF_ERROR(heap_freeChunk((pPmObj_t) pdict->d_keys));
        pdict->d_keys = C_NULL;
    }
    if (pdict->d_vals != C_NULL)
    {
        PM_RETURN_IF_ERROR(seglist_clear(pdict->d_vals));
        retval = heap_freeChunk((pPmObj_t) pdict->d_vals);
        pdict->d_vals = C_NULL;
    }
    return retval;
}


/*
 * Sets a value in the dict using the given key.
 *
 * Scans dict for the key.  If key val found, replace old
 * with new val.  If no key found, add key/val pair to dict.
 */
PmReturn_t
dict_setItem(pPmDict_t pdict, pPmObj_t pkey, pPmObj_t pval)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t indx;

    C_ASSERT(pdict != C_NULL);
    C_ASSERT(pkey != C_NULL);
    C_ASSERT(pval != C_NULL);

    /* If it's not a dict, raise TypeError */
    if (OBJ_GET_TYPE(pdict) != OBJ_TYPE_DIC)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* #112: Force Dict keys to be of hashable type */
    /* If key is not hashable, raise TypeError */
    if (OBJ_GET_TYPE(pkey) > OBJ_TYPE_HASHABLE_MAX)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* #147: Change boolean keys to integers */
    if (pkey == PM_TRUE)
    {
        pkey = PM_ONE;
    }
    else if (pkey == PM_FALSE)
    {
        pkey = PM_ZERO;
    }

    /*
     * #115: If this is the first key/value pair to be added to the Dict,
     * allocate the key and value seglists that hold those items
     */
    if (pdict->length == 0)
    {
        retval = seglist_new(&(pdict->d_keys));
        PM_RETURN_IF_ERROR(retval);
        retval = seglist_new(&(pdict->d_vals));
        PM_RETURN_IF_ERROR(retval);
    }
    else
    {
        /* Check for matching key */
        indx = 0;
        retval = seglist_findEqual(pdict->d_keys, pkey, &indx);

        /* If found a matching key, replace val obj */
        if (retval == PM_RET_OK)
        {
            retval = seglist_setItem(pdict->d_vals, pval, indx);
            return retval;
        }
    }

    /* Otherwise, insert the key,val pair */
    retval = seglist_insertItem(pdict->d_keys, pkey, 0);
    PM_RETURN_IF_ERROR(retval);
    retval = seglist_insertItem(pdict->d_vals, pval, 0);
    pdict->length++;

    return retval;
}


PmReturn_t
dict_getItem(pPmDict_t pdict, pPmObj_t pkey, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t indx = 0;

#ifdef HAVE_PROFILER
    volatile dictionary_profile *dictprofile;
    gVmGlobal.profiler_flags[IN_GETITEM] = true;

    // get the current dictionary profile
    dictprofile = profiler_get_dictprofile();

    dictprofile->lookups++;
#endif

    C_ASSERT(pdict != C_NULL);

    /* if it's not a dict, raise TypeError */
    if (OBJ_GET_TYPE(pdict) != OBJ_TYPE_DIC)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* if dict is empty, raise KeyError */
    if (pdict->length <= 0)
    {
        PM_RAISE_WITH_OBJ(retval, PM_RET_EX_KEY, pkey);
        return retval;
    }

    /* #147: Change boolean keys to integers */
    if (pkey == PM_TRUE)
    {
        pkey = PM_ONE;
    }
    else if (pkey == PM_FALSE)
    {
        pkey = PM_ZERO;
    }

    /* check for matching key */
    retval = seglist_findEqual(pdict->d_keys, pkey, &indx);

    // we searched indx + 1 number of items in seglist_findEqual
#ifdef HAVE_PROFILER
    dictprofile->entries_walked += (indx + 1);
    dictprofile->entries_total += (((pPmDict_t)pdict)->length);
#endif

    /* if key not found, raise KeyError */
    if (retval == PM_RET_NO)
    {  
        PM_RAISE_WITH_OBJ(retval, PM_RET_EX_KEY, pkey);
    }
    /* return any other error */
    PM_RETURN_IF_ERROR(retval);

    /* key was found, get obj from vals */
    retval = seglist_getItem(pdict->d_vals, indx, r_pobj);
    
#ifdef HAVE_PROFILER
    dictprofile->hits++;
    gVmGlobal.profiler_flags[IN_GETITEM] = false;
#endif

    return retval;
}


#ifdef HAVE_DEL
PmReturn_t
dict_delItem(pPmDict_t pdict, pPmObj_t pkey)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t indx = 0;

    C_ASSERT(pdict != C_NULL);

    /* Check for matching key */
    retval = seglist_findEqual(pdict->d_keys, pkey, &indx);

    /* Raise KeyError if key is not found */
    if (retval == PM_RET_NO)
    {
        PM_RAISE(retval, PM_RET_EX_KEY);
    }

    /* Return any other error */
    PM_RETURN_IF_ERROR(retval);

    /* Remove the key and value */
    retval = seglist_removeItem(pdict->d_keys, indx);
    PM_RETURN_IF_ERROR(retval);
    retval = seglist_removeItem(pdict->d_vals, indx);

    /* Reduce the item count */
    pdict->length--;

    return retval;
}
#endif /* HAVE_DEL */


#ifdef HAVE_PRINT
PmReturn_t
dict_print(pPmDict_t pdict)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t index;
    pSeglist_t keys, vals;
    pPmObj_t pobj1;

    C_ASSERT(pdict != C_NULL);

    /* if it's not a dict, raise TypeError */
    if (OBJ_GET_TYPE(pdict) != OBJ_TYPE_DIC)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    if (-1 == lib_printf("{"))
    {
        PM_RAISE(retval, PM_RET_EX_IO);
        return retval;
    }

    keys = pdict->d_keys;
    vals = pdict->d_vals;

    /* if dict is empty, raise KeyError */
    for (index = 0; index < pdict->length; index++)
    {
        if (index != 0)
        {
            if (-1 == lib_printf(", "))
            {
                PM_RAISE(retval, PM_RET_EX_IO);
                return retval;
            }
        }
        retval = seglist_getItem(keys, index, &pobj1);
        PM_RETURN_IF_ERROR(retval);
        retval = obj_print(pobj1, 1);
        PM_RETURN_IF_ERROR(retval);

        if (-1 == lib_printf(": "))
        {
            PM_RAISE(retval, PM_RET_EX_IO);
            return retval;
        }

        retval = seglist_getItem(vals, index, &pobj1);
        PM_RETURN_IF_ERROR(retval);
        retval = obj_print(pobj1, 1);
        PM_RETURN_IF_ERROR(retval);
    }

    if (-1 == lib_printf("}"))
    {
        PM_RAISE(retval, PM_RET_EX_IO);
        return retval;
    }

    return retval;
}
#endif /* HAVE_PRINT */

PmReturn_t
dict_update(pPmDict_t pdestdict, pPmDict_t psourcedict)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i;
    pPmObj_t pkey;
    pPmObj_t pval;

    C_ASSERT(pdestdict != C_NULL);
    C_ASSERT(psourcedict != C_NULL);

    /* If it's not a dict, raise TypeError */
    if (OBJ_GET_TYPE(pdestdict) != OBJ_TYPE_DIC)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* If it's not a dict, raise TypeError */
    if (OBJ_GET_TYPE(psourcedict) != OBJ_TYPE_DIC)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Iterate over the add-on dict */
    for (i = 0; i < psourcedict->length; i++)
    {
        /* Get the key,val from the add-on dict */
        retval = seglist_getItem(psourcedict->d_keys, i, &pkey);
        PM_RETURN_IF_ERROR(retval);
        retval = seglist_getItem(psourcedict->d_vals, i, &pval);
        PM_RETURN_IF_ERROR(retval);

        /* Set the key,val to the destination dict */
        retval = dict_setItem(pdestdict, pkey, pval);
        PM_RETURN_IF_ERROR(retval);
    }

    return retval;
}
