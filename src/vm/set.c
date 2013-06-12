/* vm/int.c
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x1A

#include "pm.h"

PmReturn_t
set_new(pPmSet_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmSet_t pset = C_NULL;

    /* Allocate a set */
    retval = heap_getChunk(sizeof(PmSet_t), (uint8_t **)r_pobj);
    PM_RETURN_IF_ERROR(retval);

    /* Set set type, empty the contents */
    pset = *r_pobj;
    OBJ_SET_TYPE(pset, OBJ_TYPE_SET);
    pset->length = 0;

    /* Create empty seglist */
    retval = seglist_new(&pset->val);
    return retval;
}

PmReturn_t
set_add(pPmSet_t pset, pPmObj_t pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t r_index = 0;
    
    C_ASSERT(pset != C_NULL);
    C_ASSERT(pobj != C_NULL);

    /* If pset is not a set, raise a TypeError exception */
    if (OBJ_GET_TYPE(pset) != OBJ_TYPE_SET)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected a set");
        return retval;
    }
    
    /* Check if object is already in set */
    if (seglist_findEqual(pset->val, pobj, &r_index) == PM_RET_OK) // pobj is in set
    {
        return retval;
    }
    
    else
    { /* Object not in set */

        /* Add object to set */
        retval = seglist_appendItem(pset->val, pobj);
        PM_RETURN_IF_ERROR(retval);

        /* Increment set length */
        pset->length++;

        return retval;
    }
}


PmReturn_t 
set_getItem(pPmSet_t pset, int16_t index, pPmObj_t *r_pobj)
{
    PmReturn_t retval;
    
    /* If it's not a set, raise a TypeError */
    if (OBJ_GET_TYPE(pset) != OBJ_TYPE_SET)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Adjust the index */
    if (index < 0)
    {
        index += pset->length;
    }
    
    /* Check the bounds of the index */
    if ((index < 0) || (index >= pset->length))
    {
        PM_RAISE(retval, PM_RET_EX_INDX);
        return retval;
    }

    /* Get item from seglist */
    retval = seglist_getItem(pset->val, index, r_pobj);
    return retval;
}

PmReturn_t 
set_discard(pPmSet_t pset, pPmObj_t pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t r_index = 0;
    
    C_ASSERT(pset != C_NULL);
    C_ASSERT(pobj != C_NULL);

    /* If pset is not a set, raise a TypeError exception */
    if (OBJ_GET_TYPE(pset) != OBJ_TYPE_SET)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected a set");
        return retval;
    }
    
     /* Check if object is in set */
    if (seglist_findEqual(pset->val, pobj, &r_index) == PM_RET_OK) // pobj is in set
    {
        retval = seglist_removeItem(pset->val, r_index);
        PM_RETURN_IF_ERROR(retval);
 
        /* Decrement set length */
        pset->length--;

        return retval;
    }

    else // pobj is not in set; nothing to remove
    {
        return retval;
    }

}

PmReturn_t
set_intersection(pPmSet_t pset, pPmSet_t pset2, pPmSet_t *r_set)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i;
    pPmObj_t r_pobj;
    pPmSet_t presult;

    C_ASSERT(pset != C_NULL);
    C_ASSERT(pset2 != C_NULL);

    /* If pset or pset2 is not a set, raise a TypeError exception */
    if ((OBJ_GET_TYPE(pset) != OBJ_TYPE_SET) || (OBJ_GET_TYPE(pset2) != OBJ_TYPE_SET))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected a set");
        return retval;
    }

    retval = set_new(&presult);
    PM_RETURN_IF_ERROR(retval);

    for (i = 0; i < pset->length; i++)
    {
        retval = set_getItem(pset, i, &r_pobj);
        PM_RETURN_IF_ERROR(retval);
        
        if (obj_isIn((pPmObj_t)pset2, r_pobj) == PM_RET_OK)
        {
            retval = set_add(presult, r_pobj);
            PM_RETURN_IF_ERROR(retval);
        }
    }
    
    *r_set = presult;

    return retval;
}

PmReturn_t
set_union(pPmSet_t pset, pPmSet_t pset2, pPmSet_t *r_pset)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t    i;
    pPmObj_t   r_pobj;
    pPmSet_t   presult;

    C_ASSERT(pset != C_NULL);
    C_ASSERT(pset2 != C_NULL);

    /* If pset or pset2 is not a set, raise a TypeError exception */
    if ((OBJ_GET_TYPE(pset) != OBJ_TYPE_SET) || (OBJ_GET_TYPE(pset2) != OBJ_TYPE_SET))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected a set");
        return retval;
    }

    retval = set_new(&presult);
    PM_RETURN_IF_ERROR(retval);

    for (i = 0; i < pset->length; i++)
    {
        retval = set_getItem(pset, i, &r_pobj);
        PM_RETURN_IF_ERROR(retval);

        retval = set_add(presult, r_pobj); // set_add prevents duplicates
        PM_RETURN_IF_ERROR(retval);
    }

    for (i = 0; i < pset2->length; i++)
    {
        retval = set_getItem(pset2, i, &r_pobj);
        PM_RETURN_IF_ERROR(retval);

        retval = set_add(presult, r_pobj); // set_add prevents duplicates
        PM_RETURN_IF_ERROR(retval);
    }

    *r_pset = presult;

    return retval;
}

PmReturn_t
set_difference(pPmSet_t pset, pPmSet_t pset2, pPmSet_t *r_set)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i;
    pPmObj_t r_pobj;
    pPmSet_t presult;

    C_ASSERT(pset != C_NULL);
    C_ASSERT(pset2 != C_NULL);

    /* If pset or pset2 is not a set, raise a TypeError exception */
    if ((OBJ_GET_TYPE(pset) != OBJ_TYPE_SET) || (OBJ_GET_TYPE(pset2) != OBJ_TYPE_SET))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected a set");
        return retval;
    }

    retval = set_new(&presult);
    PM_RETURN_IF_ERROR(retval);

    i = 0;
    
    for (i = 0; i < pset->length; i++)
    {
        retval = set_getItem(pset, i, &r_pobj);
        PM_RETURN_IF_ERROR(retval);

        if (obj_isIn((pPmObj_t)pset2, r_pobj) == PM_RET_NO)
        {
            retval = set_add(presult, r_pobj);
            PM_RETURN_IF_ERROR(retval);
        }
    }

    *r_set = presult;

    return retval;

}

PmReturn_t 
set_remove(pPmSet_t pset, pPmObj_t pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t r_index = 0;
    
    C_ASSERT(pset != C_NULL);
    C_ASSERT(pobj != C_NULL);

    /* If pset is not a set, raise a TypeError exception */
    if (OBJ_GET_TYPE(pset) != OBJ_TYPE_SET)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong arguments, expected a set");
        return retval;
    }
    
     /* Check if object is in set */
    if (seglist_findEqual(pset->val, pobj, &r_index) == PM_RET_OK) // pobj is in set
    {
        retval = seglist_removeItem(pset->val, r_index);
        PM_RETURN_IF_ERROR(retval);
 
        /* Decrement set length */
        pset->length--;

        return retval;
    }

    else // pobj is not in set; nothing to remove
    {
        PM_RAISE_WITH_OBJ(retval, PM_RET_EX_KEY, pobj);
        return retval;
    }
}

int8_t
set_isEqual(pPmSet_t pset1, pPmSet_t pset2)
{
    int16_t  l1;
    int16_t  l2;
    int16_t  i;
    pPmObj_t r_pobj;

    if ((OBJ_GET_TYPE(pset1) != OBJ_TYPE_SET) || (OBJ_GET_TYPE(pset2) != OBJ_TYPE_SET))
    {
        /* If pset1 or pset2 is not a set, they are not equal */
        return C_NEQ;
    }

    l1 = pset1->length;
    l2 = pset2->length;

    if (l1 != l2)
    {
        /* Sets of unequal size can't be equal */
        return C_NEQ;
    }

    for (i = 0; i < pset1->length; i++)
    {
        if (set_getItem(pset1, i, &r_pobj) != PM_RET_OK)
        {
            /* Should not happen! No way to throw exception. */
            return C_NEQ;
        }

        if (obj_isIn((pPmObj_t)pset2, r_pobj) != PM_RET_OK)
        {
            /* Missing object */
            return C_NEQ;
        }
    }

    return C_EQ;
}
