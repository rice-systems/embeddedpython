/* vm/img.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#ifndef __IMG_H__
#define __IMG_H__


/**
 * \file
 * \brief Image header
 *
 * Created to eliminate a circular include
 * among mem, string and obj.
 */


/** The maximum number of paths available in PmImgPaths */
#define PM_NUM_IMG_PATHS 4


typedef struct PmImgPaths_s
{
    uint8_t const *pimg[PM_NUM_IMG_PATHS];
    uint8_t pathcount;
}
PmImgPaths_t, *pPmImgPaths_t;


/**
 * Code image object
 *
 * A type to hold code images in the heap.
 * A code image with an object descriptor at the front.
 * Used for storing image objects during ipm;
 * the code object keeps a reference to this object.
 */
typedef struct PmCodeImgObj_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    uint8_t  hexbyte[2];
    uint16_t size;
    uint16_t i;

    /** Null-term? char array */
    uint8_t val[1];
} PmCodeImgObj_t,
 *pPmCodeImgObj_t;


/**
 * Iterates over all paths in the paths array until the named module is found.
 * Returns the address of the head of the module.
 *
 * @param pname Pointer to the name of the desired module
 * @param r_imgaddr Return by reference the address of the module's image
 * @return Return status
 */
PmReturn_t img_findInPaths(pPmString_t pname, uint8_t const **r_imgaddr);

/**
 * Appends the given address to the image path array
 *
 * @param paddr The address
 * @return Return status
 */
PmReturn_t img_appendToPath(uint8_t *paddr);

#endif /* __IMG_H__ */
