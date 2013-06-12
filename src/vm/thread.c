/* vm/thread.c
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
#define __FILE_ID__ 0x16


/**
 * \file
 * \brief VM Thread
 *
 * Encapsulating a frame pointer, a root code object and thread state.
 */


#include "pm.h"


PmReturn_t
thread_new(pPmObj_t pframe, pPmObj_t *r_pobj)
{
    PmReturn_t retval = PM_RET_OK;
    pPmThread_t pthread = C_NULL;
    pPmInt_t  ptid = C_NULL;

    C_ASSERT(pframe != C_NULL);

    /* If it's not a frame, raise TypeError */
    if (OBJ_GET_TYPE(pframe) != OBJ_TYPE_FRM)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Allocate a thread */
    retval = heap_getChunk(sizeof(PmThread_t), (uint8_t **)r_pobj);
    PM_RETURN_IF_ERROR(retval);

    /* Set type, frame and initialize status */
    pthread = (pPmThread_t)*r_pobj;
    OBJ_SET_TYPE(pthread, OBJ_TYPE_THR);
    pthread->pframe = (pPmFrame_t)pframe;
    pthread->pcfn = C_NULL;
    pthread->bytecodes = 0;
    pthread->nativecalls = 0;
    pthread->interpctrl = INTERP_CTRL_RUN;

    /* Set thread ID */
    pthread->ptid = C_NULL;
    PM_RETURN_IF_ERROR(retval);
    retval = int_new(gVmGlobal.next_tid++, (pPmInt_t *) &ptid);
    PM_RETURN_IF_ERROR(retval);

    pthread->ptid = ptid;

    /* Set the live thread flag to 1 (live) */
    pthread->liveflag = 1;

    return retval;
}

PmReturn_t
thread_addThread(pPmFunc_t pfunc)
{
    return thread_addThreadWithArg(pfunc, C_NULL, C_NULL);
}

PmReturn_t
thread_addThreadWithArg(pPmFunc_t pfunc, pPmObj_t arg, pPmObj_t *r_pthd)
{
    PmReturn_t retval;
    pPmObj_t pframe;
    pPmObj_t pthread;
    uint8_t argcount;
    uint8_t native;
    pPmObj_t pobj;

    /* Determine the number of arguments expected by the function. */
    pobj = (pPmObj_t) pfunc->f_co;
    argcount = 0;
    native = 0;
    if (IS_CODE_OBJ(pobj))
    {
        argcount = co_getArgcount(((pPmCo_t)pobj));
        native = 0;
    }
    else if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_NOB)
    {
        argcount = ((pPmNo_t)pobj)->no_argcount;
        native = 1;
    }
    else
    {
        /* Should not be possible to get here */
        return PM_RET_ERR;
    }

    /* Confirm that the appropriate number of arguments have been passed. */
    if (argcount == 0)
    {
        /* Accept C_NULL or None for 0 argument functions */
        if (! ((arg == C_NULL) || (OBJ_GET_TYPE(arg) == OBJ_TYPE_NON)))
        {
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE,
                               "incorrect number of arguments to thread function");
            return retval;
        }
        arg = C_NULL;
    }
    else if ((argcount == 1) && (arg == C_NULL))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE,
                           "incorrect number of arguments to thread function");
        return retval;
    }
    else if (argcount > 1)
    {
        /* This catches native functions because their argument counts
         * are not set correctly 
         */
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE,
                           "can only have thread functions with 0 or 1 arguments");
        return retval;
    }

    /* RIXNER: The following does not work with native functions, so
     * raise type error for now.
     */

    if (native)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE,
                           "can't currently spawn a thread with a native function");
        return retval;
    }

    /* Create a frame for the func */
    retval = frame_new((pPmObj_t)pfunc, &pframe);
    PM_RETURN_IF_ERROR(retval);

    /* Create a thread with this new frame */
    retval = thread_new(pframe, &pthread);
    PM_RETURN_IF_ERROR(retval);

    /* Add argument to frame, if present */
    if (arg != C_NULL)
    {
        ((pPmFrame_t) pframe)->fo_stack[0] = arg;
    }

    /* Return TID, if requested */
    if (r_pthd)
    {
        *r_pthd = (pPmObj_t)pthread;
    }

    /* Set the live thread flag to 1 (live) */
    ((pPmThread_t)pthread)->liveflag = 1; 

    /* Add thread to end of list */
    return list_append(gVmGlobal.threadList, pthread);
}

PmReturn_t 
thread_destroy(pPmThread_t pthd)
{
    PmReturn_t retval = PM_RET_OK;
    
    /* If it's not a thread, raise TypeError */
    if (OBJ_GET_TYPE(pthd) != OBJ_TYPE_THR)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Clear constituant objects for GC */
    pthd->pframe = C_NULL;

    /* Set the live thread flag to 0 (dead) */
    pthd->liveflag = 0;

    return retval;
}

#ifdef HAVE_PRINT
PmReturn_t
thread_print(pPmThread_t pthd)
{
    PmReturn_t retval = PM_RET_OK;

    /* Check if the thread is dead */
    if (pthd->liveflag == 0)
    {
        // TODO: oh yes you can...
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "cannot print dead thread");
        return retval;
    }

    /* If it's not a thread, raise TypeError */
    if (OBJ_GET_TYPE(pthd) != OBJ_TYPE_THR)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* print the thread id */
    lib_printf("Thread id: %d", pthd->ptid->val);

    /* print the bytecode statistics */
    lib_printf(", bytecodes: ");
    lib_printf("%d",pthd->bytecodes);
   
    /* print the nativecalls statistics */
    lib_printf(", nativecalls: ");
    lib_printf("%d",pthd->nativecalls);
    
    return retval;
}
#endif /* HAVE_PRINT */
