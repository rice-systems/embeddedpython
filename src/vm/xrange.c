/* vm/xrange.c
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x19

#include "pm.h"

PmReturn_t
xrange_new(uint16_t length, int16_t start, int16_t step, pPmXrange_t *r_pxrange)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t size = 0;

    size = sizeof(PmXrange_t);

    /* Allocate */
    retval = heap_getChunk(size, (uint8_t **)r_pxrange);
    PM_RETURN_IF_ERROR(retval);
    OBJ_SET_TYPE(*r_pxrange, OBJ_TYPE_XRA);

    (*r_pxrange)->length = length;
    (*r_pxrange)->start = start;
    (*r_pxrange)->step = step;

    /* No need to null the ptrs because they are set by the caller */
    return retval;
}


PmReturn_t
xrange_getItem(pPmXrange_t pxra, int16_t index, pPmInt_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t length;
    int32_t start, step;

    length = pxra->length;
    start  = pxra->start;
    step   = pxra->step;

    if (index < 0) {
        index = length + index;
    }

    if ((index >= length) || (index < 0)) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL,
            "index out of range");
        return retval;
    }

    retval = int_new(start+(step*index), r_pobj);

    return retval;
}

