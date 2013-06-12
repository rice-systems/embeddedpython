/* vm/module.c
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
#define __FILE_ID__ 0x0E


/**
 * \file
 * \brief Module Object Type
 *
 * Module object type operations.
 */


#include "pm.h"


PmReturn_t
mod_new(pPmObj_t pco, pPmObj_t *pmod)
{
    PmReturn_t retval;
    uint8_t *pchunk;
    pPmDict_t pattrs;

    /* If it's not a code obj, raise TypeError */
    if (!IS_CODE_OBJ(pco))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Alloc and init func obj */
    retval = heap_getChunk(sizeof(PmFunc_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    *pmod = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(*pmod, OBJ_TYPE_MOD);
    ((pPmFunc_t)*pmod)->f_co = (pPmCo_t)pco;

    /* Alloc and init attrs dict */
    retval = dict_new(&pattrs);
    ((pPmFunc_t)*pmod)->f_attrs = pattrs;

    /* A module's globals is the same as its attrs */
    ((pPmFunc_t)*pmod)->f_globals = pattrs;

#ifdef HAVE_DEFAULTARGS
    /* Clear the default args (only used by funcs) */
    ((pPmFunc_t)*pmod)->f_defaultargs = C_NULL;
#endif /* HAVE_DEFAULTARGS */

#ifdef HAVE_CLOSURES
    /* Clear the closure */
    ((pPmFunc_t)*pmod)->f_closure = C_NULL;
#endif /* HAVE_CLOSURES */

    return retval;
}


PmReturn_t
mod_import(pPmObj_t pstr, pPmObj_t *pmod)
{
    uint8_t const *imgaddr = C_NULL;
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pobj;

    /* If it's not a string obj, raise SyntaxError */
    if (OBJ_GET_TYPE(pstr) != OBJ_TYPE_STR)
    {
        PM_RAISE(retval, PM_RET_EX_SYNTAX);
        return retval;
    }

    /* Try to find the image in the paths */
    retval = img_findInPaths((pPmString_t) pstr, &imgaddr);

    /* If img was not found, raise ImportError */
    if (retval == PM_RET_NO)
    {
#ifdef HAVE_FILESYSTEM_IMPORTS
        retval = plat_fs_import((pPmString_t) pstr, &imgaddr);
        PM_RETURN_IF_ERROR(retval);
#else
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_IMPRT, "couldn't find module");
        return retval;
#endif
    }

    /* Create module from image */
    pobj = (pPmObj_t) imgaddr;
    return mod_new(pobj, pmod);
}
