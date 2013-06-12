/* vm/packtuple.h
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __PACKTUPLE_H__
#define __PACKTUPLE_H__


/**
 * \file
 * \brief Packed Tuple Object Type
 *
 * Packed Tuple object type header.
 */

/**
 * Packed Tuple obj
 *
 * Immutable ordered sequence.  Contains array of objs.
 */
typedef struct PmPackTuple_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /* number of objects in array */
    int16_t length;

    /* byte size of array */
    uint16_t size;

    /** Array of objs */
    uint8_t array[1];
} PmPackTuple_t,
 *pPmPackTuple_t;


/**
 * Checks that the objects inside of ptup are packable and calls pack. 
 * Returns a pointer to the Packed Tuple.
 *
 * @param   ptup the tuple of elements the packed tuple will contain
 * @param   r_ptp Return by ref, ptr to new packed tuple
 * @return  Return status
 */
PmReturn_t packtuple_packSetup(pPmTuple_t ptup, pPmPackTuple_t *r_pptp);

/**
 * Allocates space for a new Packed Tuple. Calls getSize and packcopy.
 * Returns a pointer to the Packed Tuple.
 *
 * @param   ptup the tuple of elements the packed tuple will contain
 * @param   r_ptp Return by ref, ptr to new packed tuple
 * @return  Return status
 */
PmReturn_t packtuple_pack(pPmTuple_t ptup, pPmPackTuple_t *r_pptp);

/**
 * Copies the objects into the already allocated packed tuple.
 *
 * @param   pdst Ptr to where to pack the elements
 * @param   ptup the tuple of elements the packed tuple will contain
 * @return  Return status
 */
PmReturn_t packtuple_packcopy(uint8_t *pdst, pPmTuple_t ptup);

/**
 * Returns the size of the entire tuple to be packed.
 *
 * @param   pobj Ptr to tuple to be sized.
 * @param   size Returned size of entire tuple and the objects it holds
 * @return  Return status
 */
PmReturn_t packtuple_getSize(pPmObj_t pobj, uint16_t *size);

/**
 * Replicates a packed tuple, n number of times to create a new packed tuple
 *
 * Copies the objects.
 *
 * @param   pptp Ptr to source packed tuple.
 * @param   n Number of times to replicate the packed tuple.
 * @param   r_pptp Return arg; Ptr to new packed tuple.
 * @return  Return status
 */
PmReturn_t packtuple_replicate(pPmPackTuple_t pptp, int16_t n, pPmPackTuple_t *r_pptp);

/**
 * Gets the object in the packed tuple at the index.
 *
 * @param   pptp Ptr to packed tuple obj
 * @param   index Index into packed tuple
 * @param   r_pobj Return by reference; ptr to item
 * @return  Return status
 */
PmReturn_t packtuple_getItem(pPmPackTuple_t pptp, int16_t index, pPmObj_t *r_pobj);

#ifdef HAVE_SLICING
/* slices a tuple */
PmReturn_t packtuple_slice(pPmPackTuple_t pptp, int16_t start, int16_t end, pPmObj_t *r_pptp);
#endif /* HAVE_SLICING */

#endif /* __PACKTUPLE_H__ */
