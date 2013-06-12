/* vm/thread.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __THREAD_H__
#define __THREAD_H__


/**
 * \file
 * \brief VM Thread
 *
 * Encapsulating a frame pointer, a root code object and thread state.
 */


#include "interp.h"


 /** Frequency in Hz to switch threads */
#define THREAD_RESCHEDULE_FREQUENCY    10


/**
 * Interpreter return values
 *
 * Used to control interpreter loop
 * and indicate return value.
 * Negative values indicate erroneous results.
 * Positive values indicate "continue interpreting",
 * but first do something special like reschedule threads
 * or (TBD) sweep the heap.
 */
typedef enum PmInterpCtrl_e
{
    /* other erroneous exits go here with negative values */
    INTERP_CTRL_ERR = -1,    /**< Generic error causes exit */
    INTERP_CTRL_EXIT = 0,    /**< Normal execution exit */
    INTERP_CTRL_RUN = 1,     /**< Continue interpreting */
    INTERP_CTRL_RESCHED = 2, /**< Reschedule threads */
    INTERP_CTRL_CYIELD = 3,  /**< Reschedule threads and continue C later */
    INTERP_CTRL_CCONT = 4,    /**< Continue "interrupted" C function */
    INTERP_CTRL_WAIT = 5   /** TODO: what are the exact semantics of this?!?! **/
        /* all positive values indicate "continue interpreting" */
} PmInterpCtrl_t, *pPmInterpCtrl_t;

/*
 * Type signature for C continuation functions.
 * These functions take a pointer to the top of the Python stack.
 */
typedef PmReturn_t (*continuefn)(pPmObj_t *);

/**
 * Thread obj
 *
 */
typedef struct PmThread_s
{
    /** object descriptor */
    PmObjDesc_t od;

    /** current frame pointer */
    pPmFrame_t pframe;

    /** thread ID */
    pPmInt_t ptid;

    /** C continuation function */
    continuefn pcfn;

    /** Statistics */
    uint32_t bytecodes;
    uint32_t nativecalls;

    /** Live thread flag (1 for live, 0 for dead) */
    uint8_t liveflag;

    /**
     * Interpreter loop control value
     *
     * A positive value means continue interpreting.
     * A zero value means normal interpreter exit.
     * A negative value signals an error exit.
     */
    PmInterpCtrl_t interpctrl;
} PmThread_t,
 *pPmThread_t;


/**
 * Constructs a thread for a root frame.
 *
 * @param  pframe Frame object as a basis for this thread.
 * @param  r_pobj Return by reference; Ptr to the newly created thread object.
 * @return Return status
 */
PmReturn_t thread_new(pPmObj_t pframe, pPmObj_t *r_pobj);

/**
 * Creates a thread object and adds it to the queue of threads to be
 * executed while interpret() is running.
 *
 * The given obj may be a function, module, or class.
 * Creates a frame for the given function.
 *
 * @param pfunc Ptr to function to be executed as a thread.
 * @return Return status
 */
PmReturn_t thread_addThread(pPmFunc_t pfunc);
PmReturn_t thread_addThreadWithArg(pPmFunc_t pfunc, pPmObj_t arg, pPmObj_t *r_ptid);

/**
 * Nulls pframe, psavequeue, and pmailbox of the passed in thread.
 *
 * @param  pthd Thread object to have the fields nulled
 * @return Return status
 */
PmReturn_t thread_destroy(pPmThread_t pthd);

#ifdef HAVE_PRINT
/**
 * Prints out information about the thread. Uses obj_print() to print 
 * elements in the message queue and for the thread id.
 *
 * @param pthd Thread object to print
 * @return Return status
 */
PmReturn_t thread_print(pPmThread_t pthd);
#endif /* HAVE_PRINT */

#endif /* __THREAD_H__ */
