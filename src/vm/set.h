/* vm/set.h
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __SET_H__
#define __SET_H__

/**
 * Set obj — Unordered collections of unique elements
 *
 */
typedef struct PmSet_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Set length */
    int16_t length;

    /** Ptr to linked list of nodes */
    pSeglist_t val;
} PmSet_t,
 *pPmSet_t;

/**
 * Allocates a new Set object.
 *
 * @param   r_pobj Return; addr of ptr to obj
 * @return  Return status
 */
PmReturn_t set_new(pPmSet_t *r_pobj);

/**
 * Adds the given obj to the set. This has no effect if the element is already present.
 *
 * @param   pset Ptr to set
 * @param   pobj Ptr to item to add
 * @return  Return status
 */
PmReturn_t set_add(pPmSet_t pset, pPmObj_t pobj);

/**
 * Gets the object in the set at the index.
 *
 * @param   pset Ptr to set obj
 * @param   index Index into set
 * @param   r_pobj Return by reference; ptr to item
 * @return  Return status
 */
PmReturn_t set_getItem(pPmSet_t pset, int16_t index, pPmObj_t *r_pobj);

/**
 * Removes the given obj from the set. If the element is not a member, do nothing.
 *
 * @param   pset Ptr to the set obj
 * @param   pobj Ptr to the object to be removed
 * @return  Return status
 */
PmReturn_t set_discard(pPmSet_t pset, pPmObj_t pobj);

/**
 * Creates a new set with elements common to pset and pset2.
 *
 * @param   pset Ptr to the set obj
 * @param   pset2 Ptr to the second set obj
 * @param   r_set Return; addr of ptr to set obj
 * @return  Return status
 */
PmReturn_t set_intersection(pPmSet_t pset, pPmSet_t pset2, pPmSet_t *r_set);

/**
 * Creates a new set with elements from both pset and pset2.
 *
 * @param   pset Ptr to the set obj
 * @param   pset2 Ptr to the second set obj
 * @param   r_set Return; addr of ptr to set obj
 * @return  Return status
 */
PmReturn_t set_union(pPmSet_t pset, pPmSet_t pset2, pPmSet_t *r_set);

/**
 * Creates a new set with elements in pset but not in pset2.
 *
 * @param   pset Ptr to the set obj
 * @param   pset2 Ptr to the second set obj
 * @param   r_set Return; addr of ptr to set obj
 * @return  Return status
 */
PmReturn_t set_difference(pPmSet_t pset, pPmSet_t pset2, pPmSet_t *r_set);

/**
 * Removes the given obj from the set. If the element is not a member, 
 * raise a KeyError.
 *
 * @param   pset Ptr to the set obj
 * @param   pobj Ptr to the object to be removed
 * @return  Return status
 */
PmReturn_t set_remove(pPmSet_t pset, pPmObj_t pobj);

/**
 * Compares two sets for equality
 *
 * @param   pset1 Ptr to first set.
 * @param   pset2 Ptr to second set.
 * @return  C_EQ if the sets are equivalent, C_NEQ otherwise.
 */
int8_t set_isEqual(pPmSet_t pset1, pPmSet_t pset2);

#endif /* __SET_H__ */
