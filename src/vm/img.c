/* vm/img.c
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
#define __FILE_ID__ 0x07


/**
 * \file
 * \brief Image routines
 *
 * Created to eliminate a circular include
 * among mem, string and obj.
 */


#include "pm.h"


/*
 * Searches for a module's name in a contiguous array of images
 * in the given namespace starting at the given address.
 * A module's name is stored in the last index of the names tuple of an image.
 */
static PmReturn_t
img_findInPath(pPmString_t pname, uint8_t const **paddr)
{
    PmReturn_t     retval = PM_RET_NO;
    uint8_t const *imgtop;
    uint16_t       len;
    uint16_t       size = 0;
    pPmPackTuple_t pnames;
    pPmString_t    pmodname;

    /* Addr is top of img */
    imgtop = *paddr;

    /* Search all sequential images */
    while (OBJ_GET_TYPE((pPmObj_t)imgtop) == OBJ_TYPE_PCO)
    {
        /* Use size field to calc addr of next potential img */
        size = OBJ_GET_SIZE((pPmObj_t)imgtop);

        /* Point to names tuple */
        pnames = (pPmPackTuple_t) co_getNames((pPmCo_t)imgtop);

        /* Ensure it's a packed tuple */
        C_ASSERT(OBJ_GET_TYPE((pPmObj_t)pnames) == OBJ_TYPE_PTP);

        /* Get the last name in the tuple (it's the module's name) */
        len = pnames->length;
        retval = packtuple_getItem(pnames, len-1, (pPmObj_t *)&pmodname);
        PM_RETURN_IF_ERROR(retval);

        /* Ensure obj is a string */
        C_ASSERT(OBJ_GET_TYPE(pmodname) == OBJ_TYPE_STR);

        /* Compare names */
        if (C_EQ == string_compare(pname, pmodname))
        {
            *paddr = imgtop;
            return PM_RET_OK;
        }

        /* Calc imgtop for next iteration */
        imgtop += size;
    }
    return PM_RET_NO;
}


PmReturn_t
img_findInPaths(pPmString_t pname, uint8_t const **r_imgaddr)
{
    uint8_t i;
    PmReturn_t retval = PM_RET_NO;

    /* Search in each path in the paths */
    for (i = 0; i < gVmGlobal.imgPaths.pathcount; i++)
    {
        *r_imgaddr = gVmGlobal.imgPaths.pimg[i];
        retval = img_findInPath(pname, r_imgaddr);
        if (retval == PM_RET_NO)
        {
            continue;
        }
        else if (retval == PM_RET_OK)
        {
            break;
        }
        else
        {
            return retval;
        }
    }

    return retval;
}


PmReturn_t
img_appendToPath(uint8_t *paddr)
{
    if (gVmGlobal.imgPaths.pathcount >= PM_NUM_IMG_PATHS)
    {
        return PM_RET_NO;
    }

    gVmGlobal.imgPaths.pimg[gVmGlobal.imgPaths.pathcount] = paddr;
    gVmGlobal.imgPaths.pathcount++;

    return PM_RET_OK;
}
