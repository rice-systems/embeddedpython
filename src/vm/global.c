/* vm/global.c
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
#define __FILE_ID__ 0x05


/**
 * \file
 * \brief VM Globals
 *
 * VM globals operations.
 * PyMite's global struct def and initial values.
 */


#include "pm.h"


extern unsigned char const *stdlib_img;

static char const *constsstr = "__consts";
char *default_exception = "";


/** Most PyMite globals all in one convenient place */
volatile PmVmGlobal_t gVmGlobal;


PmReturn_t
global_init(void)
{
    PmReturn_t retval;
    uint8_t *pchunk;
    pPmObj_t pobj;
    pPmList_t pthreadlist;
    pPmDict_t pmodules;

#ifdef HAVE_IP
    pPmList_t ppackets;
#endif /* HAVE_MEDUSA */

    /* Clear the global struct */
    memset((uint8_t *)&gVmGlobal, '\0', sizeof(PmVmGlobal_t));

    /* Set the PyMite release num (for debug and post mortem) */
    gVmGlobal.pyErrFilename = C_NULL;
    gVmGlobal.errInfo = default_exception;
    
    /* Init zero */
    retval = heap_getChunk(sizeof(PmInt_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pobj = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pobj, OBJ_TYPE_INT);
    ((pPmInt_t)pobj)->val = (int32_t)0;
    gVmGlobal.pzero = (pPmInt_t)pobj;

    /* Init one */
    retval = heap_getChunk(sizeof(PmInt_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pobj = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pobj, OBJ_TYPE_INT);
    ((pPmInt_t)pobj)->val = (int32_t)1;
    gVmGlobal.pone = (pPmInt_t)pobj;

    /* Init negone */
    retval = heap_getChunk(sizeof(PmInt_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pobj = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pobj, OBJ_TYPE_INT);
    ((pPmInt_t)pobj)->val = (int32_t)-1;
    gVmGlobal.pnegone = (pPmInt_t)pobj;

    /* Init False */
    retval = heap_getChunk(sizeof(PmBoolean_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pobj = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pobj, OBJ_TYPE_BOL);
    ((pPmBoolean_t) pobj)->val = (int32_t)C_FALSE;
    gVmGlobal.pfalse = (pPmInt_t)pobj;

    /* Init True */
    retval = heap_getChunk(sizeof(PmBoolean_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pobj = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pobj, OBJ_TYPE_BOL);
    ((pPmBoolean_t) pobj)->val = (int32_t)C_TRUE;
    gVmGlobal.ptrue = (pPmInt_t)pobj;

    /* Init None */
    retval = heap_getChunk(sizeof(PmObj_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pobj = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pobj, OBJ_TYPE_NON);
    gVmGlobal.pnone = pobj;

    /* Init empty builtins */
    gVmGlobal.builtins = C_NULL;

    /* Create empty threadList */
    retval = list_new(&pthreadlist);
    gVmGlobal.threadList = pthreadlist;

    /* No initially running thread */
    gVmGlobal.prunningThread = C_NULL;

    /* Initialize native frame flag */
    gVmGlobal.nf_active = C_FALSE;

    /* Initialize node and thread ids */
    gVmGlobal.nodeid = 0;
    gVmGlobal.next_tid = 1;
    
    /* Create empty module dict */
    retval = dict_new(&pmodules);
    gVmGlobal.modules = pmodules;

    /* Init the PmImgPaths with std image info */
    gVmGlobal.imgPaths.pimg[0] = (uint8_t *)&stdlib_img;
    gVmGlobal.imgPaths.pathcount = 1;

    /* init the exception object */
    gVmGlobal.errObj = PM_NONE;

#ifdef HAVE_PROFILER
    gVmGlobal.profilerArray = C_NULL;
#endif

#ifdef HAVE_IP
    retval = list_new(&ppackets);
    gVmGlobal.incoming_packets = ppackets;
#endif /* HAVE_IP */

    return retval;
}


PmReturn_t
global_setBuiltins(pPmFunc_t pmod)
{
    if (PM_PBUILTINS == C_NULL)
    {
        /* Need to load builtins first */
        global_loadBuiltins();
    }

    /* Put builtins module in the module's attrs dict */
    return dict_setItem(pmod->f_attrs, CONST__bi, (pPmObj_t) PM_PBUILTINS);
}


PmReturn_t
global_loadBuiltins(void)
{
    PmReturn_t retval = PM_RET_OK;
    pPmString_t pstr = C_NULL;
    pPmObj_t pbimod, pconstsmod;
    char const *pconstsstr = constsstr;

    /* Import the constants */
    retval = string_new(pconstsstr, strlen(pconstsstr), &pstr);
    PM_RETURN_IF_ERROR(retval);
    retval = mod_import((pPmObj_t) pstr, &pconstsmod);
    PM_RETURN_IF_ERROR(retval);

    /* interpret constants' root code to set them */
    C_ASSERT(gVmGlobal.threadList->length == 0);
    retval = thread_addThread((pPmFunc_t)pconstsmod);
    PM_RETURN_IF_ERROR(retval);
    retval = interpret(INTERP_RETURN_ON_NO_THREADS);
    PM_RETURN_IF_ERROR(retval);

    /* Import the builtins */
    retval = mod_import(CONST__bi, &pbimod);
    PM_RETURN_IF_ERROR(retval);

    /* Builtins points to the builtins module's attrs dict,
     * currently empty */
    gVmGlobal.builtins = ((pPmFunc_t)pbimod)->f_attrs;

    /* Set None manually before trying to run any code */
    retval = dict_setItem(PM_PBUILTINS, CONSTNone, PM_NONE);
    PM_RETURN_IF_ERROR(retval);

    /* Set False manually */
    retval = dict_setItem(PM_PBUILTINS, CONSTFalse, PM_FALSE);
    PM_RETURN_IF_ERROR(retval);

    /* Set True manually */
    retval = dict_setItem(PM_PBUILTINS, CONSTTrue, PM_TRUE);
    PM_RETURN_IF_ERROR(retval);
    
    /* Must interpret builtins' root code to set the attrs */
    C_ASSERT(gVmGlobal.threadList->length == 0);
    thread_addThread((pPmFunc_t)pbimod);
    retval = interpret(INTERP_RETURN_ON_NO_THREADS);
    PM_RETURN_IF_ERROR(retval);

    /* Deallocate builtins module */
    retval = heap_freeChunk((pPmObj_t)pbimod);

    return retval;
}

PmReturn_t
global_setPyLineNum(void)
{
    PmReturn_t retval = PM_RET_OK;
    pPmCo_t codeobj = C_NULL;
    pPmFrame_t top_user_frame;
    uint16_t line = 0;

    top_user_frame = FP;

    /* Get current code object */
    codeobj = top_user_frame->fo_func->f_co;

    line = co_getLineno(codeobj, top_user_frame->fo_ip);

    /* Set file name and line number */
    gVmGlobal.pyErrFilename = co_getFilename(codeobj);
    gVmGlobal.pyErrLineNum = line;

    return retval;
}
