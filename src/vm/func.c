/* vm/func.c
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#undef __FILE_ID__
#define __FILE_ID__ 0x04


/**
 * \file
 * \brief Function Object Type
 *
 * Function object type operations.
 */


#include "pm.h"


PmReturn_t
func_new(pPmObj_t pco, pPmObj_t pglobals, pPmObj_t *r_pfunc)
{
    PmReturn_t retval = PM_RET_OK;
    pPmFunc_t pfunc = C_NULL;
    uint8_t *pchunk;
    pPmDict_t pattrs;

    C_ASSERT(IS_CODE_OBJ(pco) || OBJ_GET_TYPE(pco) == OBJ_TYPE_NOB);
    C_ASSERT(OBJ_GET_TYPE(pglobals) == OBJ_TYPE_DIC);

    /* Allocate a func obj */
    retval = heap_getChunk(sizeof(PmFunc_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pfunc = (pPmFunc_t)pchunk;

    /* Init func */
    OBJ_SET_TYPE(pfunc, OBJ_TYPE_FXN);
    pfunc->f_co = (pPmCo_t)pco;

    /* Create attrs dict for regular func (not native) */
    if (IS_CODE_OBJ(pco))
    {
        retval = dict_new(&pattrs);
        PM_RETURN_IF_ERROR(retval);
        pfunc->f_attrs = pattrs;

        /* Store the given globals dict */
        pfunc->f_globals = (pPmDict_t)pglobals;
    }
    else
    {
        pfunc->f_attrs = C_NULL;
        pfunc->f_globals = C_NULL;
    }

#ifdef HAVE_DEFAULTARGS
    /* Clear default args (will be set later, if at all) */
    pfunc->f_defaultargs = C_NULL;
#endif /* HAVE_DEFAULTARGS */

#ifdef HAVE_CLOSURES
    /* Clear field for closure tuple */
    pfunc->f_closure = C_NULL;
#endif /* HAVE_CLOSURES */

#ifdef HAVE_PROFILER
    pfunc->samples = 0;
    pfunc->samples_nested = 0;
    pfunc->calls = 0;
#endif

    *r_pfunc = (pPmObj_t)pfunc;
    return PM_RET_OK;
}
