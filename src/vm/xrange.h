/* vm/xrange.h
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __XRANGE_H__
#define __XRANGE_H__

#include "int.h"

/**
 * \file
 * \brief xrange Object Type
 *
 * xrange object type header.
 */

/**
 * Xrange obj
 *
 * Lazy implementation of range()
 */
typedef struct PmXrange_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    int16_t length;
    int32_t start;
    int32_t step;

} PmXrange_t,
 *pPmXrange_t;


PmReturn_t xrange_new(uint16_t length, int16_t start, int16_t step, pPmXrange_t *r_pxrange);
PmReturn_t xrange_getItem(pPmXrange_t pxra, int16_t index, pPmInt_t *r_pobj);

#endif /* __XRANGE_H__ */
