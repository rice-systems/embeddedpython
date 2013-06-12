/* vm/frame.c
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
#define __FILE_ID__ 0x03


/**
 * \file
 * \brief VM Frame
 *
 * VM frame operations.
 */


#include "pm.h"


PmReturn_t
frame_new(pPmObj_t pfunc, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t fsize = 0;
    int8_t stacksz = (int8_t)0;
    int8_t nlocals = (int8_t)0;
    pPmCo_t pco = C_NULL;
    pPmFrame_t pframe = C_NULL;
    uint8_t *pchunk;
    uint8_t flags;
#ifdef HAVE_CLOSURES
    uint8_t nfreevars;
    pPmTuple_t cellvars;
#endif

    /* Get fxn's code obj */
    pco = ((pPmFunc_t)pfunc)->f_co;

    /* TypeError if passed func's CO is not a true COB */
    if (!IS_CODE_OBJ(pco))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get sizes needed to calc frame size */
    stacksz = co_getStacksize(pco);
    nlocals = co_getNlocals(pco);

#ifdef HAVE_GENERATORS
    /* #207: Initializing a Generator using CALL_FUNC needs extra stack slot */
    fsize = sizeof(PmFrame_t) + (stacksz + nlocals + 2) * sizeof(pPmObj_t);
#elif defined(HAVE_CLASSES)
    /* #230: Calling a class's __init__() takes two extra spaces on the stack */
    fsize = sizeof(PmFrame_t) + (stacksz + nlocals + 1) * sizeof(pPmObj_t);
#else
    fsize = sizeof(PmFrame_t) + (stacksz + nlocals - 1) * sizeof(pPmObj_t);
#endif /* HAVE_CLASSES */

#ifdef HAVE_CLOSURES
    /* #256: Add support for closures */
    nfreevars = co_getNfreevars(pco);
    cellvars = co_getCellvars(pco);
    fsize = fsize + 
        (nfreevars + ((cellvars == C_NULL) ? 0 : tuple_getLength(cellvars))) * sizeof(pPmObj_t);
#endif /* HAVE_CLOSURES */

    /* Allocate a frame */
    retval = heap_getChunk(fsize, &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pframe = (pPmFrame_t)pchunk;

    /* Set frame fields */
    OBJ_SET_TYPE(pframe, OBJ_TYPE_FRM);
    pframe->fo_back = C_NULL;
    pframe->fo_except = C_NULL;
    pframe->fo_func = (pPmFunc_t)pfunc;

    /* Init instruction pointer, line number and block stack */
    pframe->fo_ip = co_getCodeaddr(pco);
    pframe->fo_blockstack = C_NULL;

    /* Get globals from the function object */
    pframe->fo_globals = ((pPmFunc_t)pfunc)->f_globals;

    /* see PyPy's pyframe.py:initialize_frame_scopes() */
    flags = co_getFlags(pco);
    if ((flags & (CO_NEWLOCALS | CO_OPTIMIZED)) == (CO_NEWLOCALS | CO_OPTIMIZED))
    {
        pframe->fo_locals = C_NULL;
    }
    else if (flags & CO_NEWLOCALS)
    {
        retval = dict_new(&(pframe->fo_locals));
        PM_RETURN_IF_ERROR(retval);
    }
    else
    {
        pframe->fo_locals = pframe->fo_globals;
    }

    // calculate this based on what we passed to the allocator so that even
    // if we screw up our calculation, we don't smash the stack.
#ifdef STACK_PROTECTION
    pframe->fo_last_stack_slot = (pPmObj_t) (((uint8_t *) pframe) + fsize - sizeof(pPmObj_t));
#endif

#ifndef HAVE_CLOSURES
    /* Empty stack points to one past locals */
    pframe->fo_sp = &(pframe->fo_stack[nlocals]);
#else
    /* #256: Add support for closures */
    pframe->fo_sp = &(pframe->fo_stack[nlocals + nfreevars
            + ((cellvars == C_NULL) ? 0 : tuple_getLength(cellvars))]);
#endif /* HAVE_CLOSURES */

    /* By default, this is a normal frame, not an import or __init__ one */
    pframe->fo_isImport = 0;
#ifdef HAVE_CLASSES
    pframe->fo_isInit = 0;
#endif

    /* No temporary object, initially */
    pframe->liveObj = C_NULL;

    /* Clear locals, free variables, cell variables, and the stack */
    memset((unsigned char *)&(pframe->fo_stack), (char const)0,
               (unsigned int)fsize - sizeof(PmFrame_t));

    /* Return ptr to frame */
    *r_pobj = (pPmObj_t)pframe;
    return retval;
}
