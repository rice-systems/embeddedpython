/* vm/tuple.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __TUPLE_H__
#define __TUPLE_H__


/**
 * \file
 * \brief Tuple Object Type
 *
 * Tuple object type header.
 */

/**
 * Tuple obj
 *
 * Immutable ordered sequence.  Contains array of ptrs to objs.
 */
typedef struct PmTuple_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /**
     * Length of tuple
     * I don't expect a tuple to ever exceed 255 elements,
     * but if I set this type to int8_t, a 0-element tuple
     * is too small to be allocated.
     */
    int16_t length;

    /** Array of ptrs to objs */
    pPmObj_t items[1];
} PmTuple_t,
 *pPmTuple_t;

/**
 * Allocates space for a new Tuple.  Returns a pointer to the tuple.
 *
 * @param   n the number of elements the tuple will contain
 * @param   r_ptuple Return by ref, ptr to new tuple
 * @return  Return status
 */
PmReturn_t tuple_new(uint16_t n, pPmTuple_t *r_ptuple);

/**
 * Creates a new tuple identical to ptup using obj_copy.
 * Works as unpack for a packed tuple.
 *
 * @param   ptup Ptr to source tuple (or packed tuple)
 * @param   r_ptup Return arg; Ptr to new tuple.
 * @Return  Return status
 */
PmReturn_t tuple_copy(pPmTuple_t ptup, pPmTuple_t *r_ptup);

/**
 * Replicates a tuple, n number of times to create a new tuple
 *
 * Copies the pointers (not the objects).
 *
 * @param   ptup Ptr to source tuple.
 * @param   n Number of times to replicate the tuple.
 * @param   r_ptuple Return arg; Ptr to new tuple.
 * @return  Return status
 */
PmReturn_t tuple_replicate(pPmTuple_t ptup, int16_t n, pPmObj_t *r_ptuple);

/**
 * Gets the object in the tuple at the index (or calls the method to get an object from a packed tuple.)
 *
 * @param   ptup Ptr to tuple obj (or packed tuple object)
 * @param   index Index into tuple
 * @param   r_pobj Return by reference; ptr to item
 * @return  Return status
 */
PmReturn_t tuple_getItem(pPmTuple_t ptup, int16_t index, pPmObj_t *r_pobj);

/**
 * Gets the length of a tuple (or a packed tuple)
 *
 * @param  ptup Ptr to the tuple obj (or packed tuple object)
 * @return Length of the tuple
 */
int16_t tuple_getLength(pPmTuple_t ptup);

/**
 * Gets the index in the tuple of the given object
 *
 * @param   ptup Ptr to tuple obj (or packed tuple object)
 * @param   pitem object to look for
 * @param   r_index Return by reference; index in tuple
 * @return  Return status
 */
PmReturn_t tuple_index(pPmTuple_t ptup, pPmObj_t pitem, int16_t *r_index);

#ifdef HAVE_SLICING
/* slices a tuple */
PmReturn_t tuple_slice(pPmTuple_t ptup1, int16_t start, int16_t end, pPmObj_t *r_ptuple);
#endif

#endif /* __TUPLE_H__ */
