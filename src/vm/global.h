/* vm/global.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#ifndef __GLOBAL_H__
#define __GLOBAL_H__


/**
 * \file
 * \brief VM Globals
 *
 * VM globals header.
 */


/** The global root PmGlobals Dict object */
#define PM_PBUILTINS    (gVmGlobal.builtins)

/** The global None object */
#define PM_NONE         (pPmObj_t)(gVmGlobal.pnone)

/** The global False object */
#define PM_FALSE        (pPmObj_t)(gVmGlobal.pfalse)

/** The global True object */
#define PM_TRUE         (pPmObj_t)(gVmGlobal.ptrue)

/** The global integer 0 object */
#define PM_ZERO         (pPmObj_t)(gVmGlobal.pzero)

/** The global integer 1 object */
#define PM_ONE          (pPmObj_t)(gVmGlobal.pone)

/** The global integer -1 object */
#define PM_NEGONE       (pPmObj_t)(gVmGlobal.pnegone)

#include "consts.h"

/**
 * This struct contains ALL of PyMite's globals
 */
typedef struct PmVmGlobal_s
{
    /** Global none obj (none) */
    pPmObj_t pnone;

    /** Global integer 0 obj */
    pPmInt_t pzero;

    /** Global integer 1 obj */
    pPmInt_t pone;

    /** Global integer -1 obj */
    pPmInt_t pnegone;

    /** Global boolean False obj */
    pPmInt_t pfalse;

    /** Global boolean True obj */
    pPmInt_t ptrue;

    /** Dict for builtins */
    pPmDict_t builtins;

    /** Dict for modules */
    pPmDict_t modules;

    /** Paths to available images */
    PmImgPaths_t imgPaths;

    /** PyMite source file ID number for when an error occurs */
    uint8_t errFileId;

    /** Line number for when an error occurs */
    uint16_t errLineNum;

    /** Generic information for exception */
    pPmObj_t errObj;

    /** Generic information for exception */
    char* errInfo;

    /** Thread list */
    pPmList_t threadList;

    /** Ptr to current thread */
    pPmThread_t prunningThread;

    /** the array of constant strings */
    pPmObj_t consts[NUM_CONSTANTS];

    /** Flag to trigger rescheduling */
    uint8_t reschedule;

    /** Flag to indicate that a native frame is active */
    uint8_t nf_active;

    /** Node identifier */
    uint32_t nodeid;
    
    /** Next local thread ID */
    uint32_t next_tid;

#ifdef HAVE_PROFILER
    // for the python line number profiler
    pPmProfilerArray_t profilerArray;

    // for the dictionary profiler
    dictionary_profile dictprofiles[NUM_DICTPROFILES];

    // various flags for the profiler
    bool profiler_flags[NUM_PROFILER_FLAGS];
    uint32_t profiler_frequency;
#endif

#ifdef HAVE_IP
    // for the IP stack
    pPmList_t incoming_packets;
#endif /* HAVE_IP */

} PmVmGlobal_t,
 *pPmVmGlobal_t;


extern volatile PmVmGlobal_t gVmGlobal;


/**
 * Initializes the global struct
 *
 * @return Return status
 */
PmReturn_t global_init(void);

/**
 * Sets the builtins dict into the given module's attrs.
 *
 * If not yet done, loads the "__bt" module via global_loadBuiltins().
 * Restrictions described in that functions documentation apply.
 *
 * @param pmod Module whose attrs receive builtins
 * @return Return status
 */
PmReturn_t global_setBuiltins(pPmFunc_t pmod);

/**
 * Loads the "__bt" module and sets the builtins dict (PM_PBUILTINS)
 * to point to __bt's attributes dict.
 * Creates "None" = None entry in builtins.
 *
 * When run, there should not be any other threads in the interpreter
 * thread list yet.
 *
 * @return  Return status
 */
PmReturn_t global_loadBuiltins(void);

#endif /* __GLOBAL_H__ */
