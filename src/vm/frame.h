/* vm/frame.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __FRAME_H__
#define __FRAME_H__


/**
 * \file
 * \brief VM Frame
 *
 * VM frame header.
 */


/**
 * Block Type
 *
 * Numerical values to put in the 'b_type' field of the tPmBlockType struct.
 */
typedef enum PmBlockType_e
{
    /** Invalid block type */
    B_INVALID = 0,

    /** Loop type */
    B_LOOP,

    /** Try type */
    B_TRY
} PmBlockType_t, *pPmBlockType_t;


/**
 * Block
 *
 * Extra info for loops and trys (others?)
 * Frames use linked list of blocks to handle
 * nested loops and try-catch blocks.
 */
typedef struct PmBlock_s
{
    /** Obligatory obj descriptor */
    PmObjDesc_t od;

    /** Ptr to backup stack ptr */
    pPmObj_t *b_sp;

    /** Handler fxn obj */
    uint8_t const *b_handler;

    /** Block type */
    PmBlockType_t b_type:8;

    /** Next block in stack */
    struct PmBlock_s *next;
} PmBlock_t,
 *pPmBlock_t;


/**
 * Frame
 *
 * A struct that holds the execution frame of a function, including the stack,
 * local vars and pointer to the code object.
 *
 * This struct doesn't declare the stack.
 * frame_new() is responsible for allocating the extra memory
 * at the tail of fo_stack[] to hold both the locals and stack.
 */
typedef struct PmFrame_s
{
    /** Obligatory obj descriptor */
    PmObjDesc_t od;

    /** Ptr to previous frame obj */
    struct PmFrame_s *fo_back;

    /** Ptr to exception frame obj */
    struct PmFrame_s *fo_except;

    /** Ptr to function obj */
    pPmFunc_t fo_func;

    /** Instruction pointer */
    uint8_t const *fo_ip;

    /** Linked list of blocks */
    pPmBlock_t fo_blockstack;

    /** Locals dict (non-fast locals) */
    pPmDict_t fo_locals;

    /** Global attributes dict (pts to root frame's globals */
    pPmDict_t fo_globals;

    /** Points to next empty slot in fo_stack (1 past TOS) */
    pPmObj_t *fo_sp;

    /** Frame can be an import-frame that handles RETURN differently */
    uint8_t fo_isImport:1;

#ifdef HAVE_CLASSES
    /** Flag to indicate class initailzer frame; handle RETURN differently */
    uint8_t fo_isInit:1;
#endif /* HAVE_CLASSES */

    /** Temporary pointer to a live object to protect it from GC */
    pPmObj_t liveObj;
    
    // pointer to the last possible slot in fo_stack
#ifdef STACK_PROTECTION
    pPmObj_t fo_last_stack_slot;
#endif

    /** Array of local vars and stack (space appended at alloc) */
    pPmObj_t fo_stack[1];
    /* WARNING: Do not put new fields below fo_stack */
} PmFrame_t,
 *pPmFrame_t;


/**
 * Allocate space for a new frame, fill its fields
 * with respect to the given function object.
 * Return pointer to the new frame.
 *
 * @param   pfunc ptr to Function object.
 * @param   r_pobj Return value; the new frame.
 * @return  Return status.
 */
PmReturn_t frame_new(pPmObj_t pfunc, pPmObj_t *r_pobj);

#endif /* __FRAME_H__ */
