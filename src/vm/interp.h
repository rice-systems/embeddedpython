/* vm/interp.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __INTERP_H__
#define __INTERP_H__


/**
 * \file
 * \brief VM Interpreter
 *
 * VM interpreter header.
 */


#include "thread.h"

#include "opcodes.h"


#define INTERP_LOOP_FOREVER          0
#define INTERP_RETURN_ON_NO_THREADS  1

/** running thread */
#define RUNNINGTHREAD   (gVmGlobal.prunningThread)
/** frame pointer ; currently for single thread */
#define FP              (RUNNINGTHREAD->pframe)
/** main module pointer (referred to by root frame) */
#define MP              (gVmGlobal.pmod)
/** instruction pointer */
#define IP              (FP->fo_ip)
/** argument stack pointer */
#undef SP
#define SP              (FP->fo_sp)

/** top of stack */
#define TOS             (*(SP - 1))
/** one under TOS */
#define TOS1            (*(SP - 2))
/** two under TOS */
#define TOS2            (*(SP - 3))
/** three under TOS */
#define TOS3            (*(SP - 4))
/** index into stack; 0 is top, 1 is next */
#define STACK(n)        (*(SP - ((n) + 1)))
/** pops an obj from the stack */
#define PM_POP()        (*(--SP))

/** pushes an obj on the stack */
#ifdef STACK_PROTECTION
PmReturn_t pm_push_protected(pPmObj_t pobj);

#define PM_PUSH(pobj) \
    {  \
        retval_stackp = pm_push_protected(pobj); \
        if (retval_stackp != PM_RET_OK) { \
            retval = retval_stackp; \
            break; \
        } \
    }
#else
#define PM_PUSH(pobj)   (*(SP++) = (pobj))
#endif


/* The NATIVE_ macros should only be used inside native functions */

/** pushes an obj in the only stack slot of the native frame */
#define NATIVE_SET_TOS(pobj) (*r_pobj = (pobj))
/** gets a pointer to the frame that called this native fxn */
#define NATIVE_GET_PFRAME()   (*ppframe)
/** gets the number of args passed to the native fxn */
#define NATIVE_GET_NUM_ARGS() (numlocals)
/** gets the nth local var from the native frame locals */
#define NATIVE_GET_LOCAL(n) (*(NATIVE_GET_PFRAME()->fo_sp - \
                               (NATIVE_GET_NUM_ARGS() - (n))))


/**
 * COMPARE_OP enum.
 * Used by the COMPARE_OP bytecode to determine
 * which type of compare to perform.
 * Must match those defined in Python.
 */
typedef enum PmCompare_e
{
    COMP_LT = 0,            /**< less than */
    COMP_LE,                /**< less than or equal */
    COMP_EQ,                /**< equal */
    COMP_NE,                /**< not equal */
    COMP_GT,                /**< greater than */
    COMP_GE,                /**< greater than or equal */
    COMP_IN,                /**< is in */
    COMP_NOT_IN,            /**< is not in */
    COMP_IS,                /**< is */
    COMP_IS_NOT,            /**< is not */
    COMP_EXN_MATCH,         /**< do exceptions match */
    COMP_BIND               /**< <- compare and bind all unbounds */
} PmCompare_t, *pPmCompare_t;


/**
 * Interprets the available threads. Does not return.
 *
 * @param returnOnNoThreads Loop forever if 0, exit with status if no more
 *                          threads left.
 * @return Return status if called with returnOnNoThreads != 0,
 *         will not return otherwise.
 */
PmReturn_t interpret(const uint8_t returnOnNoThreads);

/**
 * Selects a thread to run and changes the VM internal variables to
 * let the switch-loop execute the chosen one in the next iteration.
 * For the moment the algorithm is primitive and will change the
 * thread each time it is called in a round-robin fashion.
 */
PmReturn_t interp_reschedule(void);

/**
 * Sets the  reschedule flag.
 *
 * @param boolean Reschedule on next occasion if boolean is true; clear
 *                the flag otherwise.
 */
void interp_setRescheduleFlag(uint8_t boolean);

#endif /* __INTERP_H__ */
