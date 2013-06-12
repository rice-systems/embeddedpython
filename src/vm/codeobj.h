/* vm/codeobj.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#ifndef __CODEOBJ_H__
#define __CODEOBJ_H__


/**
 * \file
 * \brief CodeObj Type
 *
 * CodeObj type header.
 */


/* Masks for co_flags (from Python's code.h) */
#define CO_OPTIMIZED 0x01
#define CO_NEWLOCALS 0x02
#define CO_VARARGS 0x04
#define CO_VARKEYWORDS 0x08
#define CO_NESTED 0x10
#define CO_GENERATOR 0x20
#define CO_NOFREE 0x40

/** Code object type */

struct PmCo_s;
typedef struct PmCo_s PmCo_t, *pPmCo_t;

pPmTuple_t     co_getNames(pPmCo_t pcob);
pPmTuple_t     co_getVarNames(pPmCo_t pcob);
pPmTuple_t     co_getConsts(pPmCo_t pcob);
uint8_t        co_getStacksize(pPmCo_t pcob);
uint16_t       co_getNlocals(pPmCo_t pcob);
pPmString_t    co_getFilename(pPmCo_t pcob);
uint16_t       co_getFirstlineno(pPmCo_t pcob);
uint16_t       co_getMaxlineno(pPmCo_t pcob);
uint16_t       co_getLineno(pPmCo_t pcob, uint8_t const *fo_ip);
uint8_t const *co_getCodeaddr(pPmCo_t pcob);
uint8_t        co_getFlags(pPmCo_t pcob);
uint8_t        co_getArgcount(pPmCo_t pcob);

#ifdef HAVE_CLOSURES
uint8_t        co_getNfreevars(pPmCo_t pcob);
pPmTuple_t     co_getCellvars(pPmCo_t pcob);
#endif

/* Needed for the garbage collector, should not be used elsewhere */
pPmString_t    co_getLnotab(pPmCo_t pcob);
pPmString_t    co_getCode(pPmCo_t pcob);

/**
 * Native Code Object
 *
 * An extended object that holds only the most frequently used parts
 * of the static native image.  Other parts can be obtained by
 * inspecting the native image itself.
 */
typedef struct PmNo_s
{
    /** object descriptor */
    PmObjDesc_t od;
    /** expected num args to the func */
    int8_t no_argcount;
    /** index into native function table */
    int16_t no_funcindx;
} PmNo_t,
 *pPmNo_t;


/**
 * Copies a code object.  Takes either a packed or unpacked object.
 * Always returns an unpacked object.
 *
 * @param  pco   code object to be copied
 * @param  r_pco Return by reference, new code object 
 * @return Return status
 */
PmReturn_t co_copy(pPmCo_t pco, pPmCo_t *r_pco);

/**
 * Copies a native code object.
 *
 * @param  pno   code object to be copied
 * @param  r_pno Return by reference, new code object 
 * @return Return status
 */
PmReturn_t no_copy(pPmNo_t pno, pPmNo_t *r_pno);



uint8_t xtod_nibble(char c);
uint8_t xtod_byte(char c[2]);

#endif /* __CODEOBJ_H__ */
