/* vm/list.c
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
#define __FILE_ID__ 0x0B


/**
 * \file
 * \brief List Object Type
 *
 * List object type operations.
 */


#include "pm.h"


PmReturn_t
list_append(pPmList_t plist, pPmObj_t pobj)
{
    PmReturn_t retval;

    C_ASSERT(plist != C_NULL);
    C_ASSERT(pobj != C_NULL);

    /* If plist is not a list, raise a TypeError exception */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Append object to list */
    retval = seglist_appendItem(plist->val, pobj);
    PM_RETURN_IF_ERROR(retval);

    /* Increment list length */
    plist->length++;

    return retval;
}


PmReturn_t
list_getItem(pPmList_t plist, int16_t index, pPmObj_t *r_pobj)
{
    PmReturn_t retval;

    /* If it's not a list, raise TypeError */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Adjust the index */
    if (index < 0)
    {
        index += plist->length;
    }

    /* Check the bounds of the index */
    if ((index < 0) || (index >= plist->length))
    {
        PM_RAISE(retval, PM_RET_EX_INDX);
        return retval;
    }

    /* Get item from seglist */
    retval = seglist_getItem(plist->val, index, r_pobj);
    return retval;
}


PmReturn_t
list_insert(pPmList_t plist, int16_t index, pPmObj_t pobj)
{
    PmReturn_t retval;
    int16_t len;

    C_ASSERT(plist != C_NULL);
    C_ASSERT(pobj != C_NULL);

    /* Raise a TypeError if plist is not a List */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        PM_RETURN_IF_ERROR(retval);
    }

    /* Adjust an out-of-bounds index value */
    len = plist->length;
    if (index < 0)
    {
        index += len;
    }
    if (index < 0)
    {
        index = 0;
    }
    if (index > len)
    {
        index = len;
    }

    /* Insert the item in the container */
    retval = seglist_insertItem(plist->val, pobj, index);
    PM_RETURN_IF_ERROR(retval);

    /* Increment list length */
    plist->length++;
    return retval;
}


PmReturn_t
list_new(pPmList_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmList_t plist = C_NULL;

    /* Allocate a list */
    retval = heap_getChunk(sizeof(PmList_t), (uint8_t **)r_pobj);
    PM_RETURN_IF_ERROR(retval);

    /* Set list type, empty the contents */
    plist = *r_pobj;
    OBJ_SET_TYPE(plist, OBJ_TYPE_LST);
    plist->length = 0;

    /* Create empty seglist */
    retval = seglist_new(&plist->val);
    return retval;
}


PmReturn_t
list_copy(pPmList_t pobj, pPmList_t *r_pobj)
{
    return list_replicate(pobj, 1, r_pobj);
}


PmReturn_t
list_replicate(pPmList_t psrclist, int16_t n, pPmList_t *r_pnewlist)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i = 0;
    int16_t j = 0;
    int16_t length = 0;
    pPmObj_t pitem = C_NULL;

    C_ASSERT(psrclist != C_NULL);
    C_ASSERT(r_pnewlist != C_NULL);

    /* If first arg is not a list, raise TypeError */
    if (OBJ_GET_TYPE(psrclist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }
    length = psrclist->length;

    /* Allocate new list */
    retval = list_new(r_pnewlist);
    PM_RETURN_IF_ERROR(retval);

    /* Copy srclist the designated number of times */
    for (i = n; i > 0; i--)
    {
        /* Iterate over the length of srclist */
        for (j = 0; j < length; j++)
        {
            retval = list_getItem(psrclist, j, &pitem);
            PM_RETURN_IF_ERROR(retval);
            retval = list_append(*r_pnewlist, pitem);
            PM_RETURN_IF_ERROR(retval);
        }
    }
    return retval;
}


PmReturn_t
list_setItem(pPmList_t plist, int16_t index, pPmObj_t pobj)
{
    PmReturn_t retval;

    /* If it's not a list, raise TypeError */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Adjust the index */
    if (index < 0)
    {
        index += plist->length;
    }

    /* Check the bounds of the index */
    if ((index < 0) || (index >= plist->length))
    {
        PM_RAISE(retval, PM_RET_EX_INDX);
        return retval;
    }

    /* Set the item */
    retval = seglist_setItem(plist->val, pobj, index);
    return retval;
}


PmReturn_t
list_remove(pPmList_t plist, pPmObj_t item)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t index;

    /* If it's not a list, raise TypeError */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Locate the item to remove */
    retval = list_index(plist, item, &index);
    PM_RETURN_IF_ERROR(retval);

    /* Remove the item and decrement the list length */
    retval = seglist_removeItem(plist->val, index);
    plist->length--;
    return retval;

}


PmReturn_t
list_index(pPmList_t plist, pPmObj_t pitem, uint16_t *r_index)
{
    PmReturn_t retval = PM_RET_OK;
    pSeglist_t pseglist;
    pPmObj_t pobj;
    uint16_t index;

    /* If it's not a list, raise TypeError */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "non-list");
        return retval;
    }

    pseglist = plist->val;

    /* Iterate over the list's contents */
    for (index = 0; index < pseglist->sl_length; index++)
    {
        retval = seglist_getItem(pseglist, index, &pobj);
        PM_RETURN_IF_ERROR(retval);

        /* If the list item matches the given item, return the index */
        if (obj_isEqual(pobj, pitem) == C_EQ)
        {
            *r_index = index;
            return PM_RET_OK;
        }
    }

    PM_RAISE_WITH_OBJ(retval, PM_RET_EX_VAL, pitem);
    return retval;
}


PmReturn_t
list_delItem(pPmList_t plist, int16_t index)
{
    PmReturn_t retval = PM_RET_OK;

    /* If it's not a list, raise TypeError */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Adjust the index */
    if (index < 0)
    {
        index += plist->length;
    }

    /* Check the bounds of the index */
    if ((index < 0) || (index >= plist->length))
    {
        PM_RAISE(retval, PM_RET_EX_INDX);
        return retval;
    }

    /* Remove the item and decrement the list length */
    retval = seglist_removeItem(plist->val, index);
    plist->length--;
    return retval;
}


PmReturn_t
list_clear(pPmList_t plist)
{
    PmReturn_t retval = PM_RET_OK;

    C_ASSERT(plist != C_NULL);

    /* Raise TypeError if arg is not a dict */
    if (OBJ_GET_TYPE(plist) != OBJ_TYPE_LST)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* clear length */
    plist->length = 0;

    /* clear the keys and values seglists if needed */
    if (plist->val != C_NULL)
    {
        retval = seglist_clear(plist->val);
    }
    return retval;
}

#ifdef HAVE_SLICING
PmReturn_t
list_slice(pPmList_t plist1, int16_t start, int16_t end, pPmObj_t *r_plist)
{
    PmReturn_t retval = PM_RET_OK;
    pPmList_t plist = C_NULL;
    pPmObj_t pitem;
    uint16_t len;
    uint16_t i = 0;
    len = end - start;
    
    list_new(&plist);

    while (len > 0) {
        retval = list_getItem(plist1, start+i, &pitem);
        PM_RETURN_IF_ERROR(retval);
        retval = list_append(plist, pitem);
        PM_RETURN_IF_ERROR(retval);
        
        i++;
        len--;
    }

    *r_plist = (pPmObj_t)plist;
    return PM_RET_OK;
}
#endif /* HAVE_SLICING */
