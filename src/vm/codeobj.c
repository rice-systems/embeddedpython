/* vm/codeobj.c
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
#define __FILE_ID__ 0x01


/**
 * \file
 * \brief CodeObj Type
 *
 * CodeObj type operations.
 */


#include "pm.h"

uint16_t co_getLnotab_len(pPmCo_t pcob);

/**
 * Code Object
 *
 * Object containing everything needed to execute Python code.
 */

/**
 * Fixed size elements of a code object.
 */
struct CoFixed_s
{
    /** object descriptor */
    PmObjDesc_t od;

    /** Size of stack */
    uint8_t co_stacksize;
    /** number of positional arguments the function expects */
    uint8_t co_argcount;
    /** compiler flags */
    uint8_t co_flags;
    /** Number of local variables */
    uint8_t co_nlocals;
    /** Line number information */
    uint16_t co_firstlineno;
#ifdef HAVE_CLOSURES
    /** Number of freevars */
    uint8_t co_nfreevars;
#else
    /* Explicit pad byte */
    uint8_t _pad1;
#endif /* HAVE_CLOSURES */
    /* Explicit pad byte */
    uint8_t _pad2;
};

/**
 * Heap-based unpacked code object.
 */
struct PmCo_s
{
    struct CoFixed_s fixed;
    /** Names */
    pPmTuple_t co_names;
    /** Local Names */
    pPmTuple_t co_varnames;
    /** Constants */
    pPmTuple_t co_consts;
    /** Python file name */
    pPmString_t co_filename;
    /** Line number information */
    pPmString_t lnotab;
    /** Bytecode */
    pPmString_t code;
#ifdef HAVE_CLOSURES
    /** cell variables */
    pPmTuple_t co_cellvars;
#endif /* HAVE_CLOSURES */
};

/**
 * Flash-based packed code object.
 */
typedef struct PmPackCo_s
{
    struct CoFixed_s fixed;

    /* Packed Tuple containing Python objects */
    uint8_t packtup[1];
} *pPmPackCo_t;

#define CO_NAMES_IDX    0
#define CO_VARNAMES_IDX 1
#define CO_CONSTS_IDX   2
#define CO_FILENAME_IDX 3
#define CO_LNOTAB_IDX   4
#define CO_CODE_IDX     5
#define CO_CELLVARS_IDX 6


/** Accessor functions */

pPmTuple_t co_getNames(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->co_names;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_NAMES_IDX, &pobj);
        return (pPmTuple_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}

pPmTuple_t co_getVarNames(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->co_varnames;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_VARNAMES_IDX, &pobj);
        return (pPmTuple_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}

pPmTuple_t co_getConsts(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->co_consts;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_CONSTS_IDX, &pobj);
        return (pPmTuple_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}

uint8_t co_getStacksize(pPmCo_t pcob)
{
    return pcob->fixed.co_stacksize;
}

uint16_t co_getNlocals(pPmCo_t pcob)
{
    return pcob->fixed.co_nlocals;
}

uint16_t co_getLnotab_len(pPmCo_t pcob)
{
    pPmString_t lnotab = co_getLnotab(pcob);
    return lnotab->length;
}

uint16_t co_getFirstlineno(pPmCo_t pcob)
{
    return pcob->fixed.co_firstlineno;
}

pPmString_t co_getFilename(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->co_filename;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_FILENAME_IDX, &pobj);
        return (pPmString_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}

uint8_t const *co_getCodeaddr(pPmCo_t pcob)
{
    uint8_t *codeaddr;
    pPmString_t code = co_getCode(pcob);
    codeaddr = code->val;
    return codeaddr;
}

uint8_t co_getFlags(pPmCo_t pcob)
{
    return pcob->fixed.co_flags;
}

uint8_t co_getArgcount(pPmCo_t pcob)
{
    return pcob->fixed.co_argcount;
}

uint16_t co_getMaxlineno(pPmCo_t pcob)
{
    int16_t  size = 0;
    uint16_t lines = 0;
    uint8_t const *p;

    size = co_getLnotab_len(pcob) / 2;
    lines = co_getFirstlineno(pcob);
    p = co_getLnotab(pcob)->val;
    while (--size >= 0) {
        p++;
        lines += *p++;
    }

    return lines;
}

uint16_t co_getLineno(pPmCo_t pcob, uint8_t const *fo_ip)
{
    uint16_t bc_offset;
    int16_t  size = 0;
    uint16_t addr = 0;
    uint16_t line = 0;
    uint8_t const *p;
    
    bc_offset = fo_ip - co_getCodeaddr(pcob);
    size = co_getLnotab_len(pcob) / 2;
    line = co_getFirstlineno(pcob);
    p = co_getLnotab(pcob)->val;
    while (--size >= 0) {
        addr += *p++;
        if (addr > bc_offset)
            break;
        line += *p++;
    }

    return line;
}

#ifdef HAVE_CLOSURES
uint8_t co_getNfreevars(pPmCo_t pcob)
{
    return pcob->fixed.co_nfreevars;
}

pPmTuple_t co_getCellvars(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->co_cellvars;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_CELLVARS_IDX, &pobj);
        return (pPmTuple_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}
#endif

pPmString_t co_getLnotab(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->lnotab;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_LNOTAB_IDX, &pobj);
        return (pPmString_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}

pPmString_t co_getCode(pPmCo_t pcob)
{
    pPmObj_t pobj = C_NULL;

    switch(OBJ_GET_TYPE(pcob))
    {
    case OBJ_TYPE_COB:
        return pcob->code;
    case OBJ_TYPE_PCO:
        packtuple_getItem((pPmPackTuple_t)&(((pPmPackCo_t)pcob)->packtup), CO_CODE_IDX, &pobj);
        return (pPmString_t) pobj;
    }

    /* Should not get here */
    return C_NULL;
}

/* these functions convert stings of hex numbers into bytes. used in 
 * the serial communication in ipm and the bootloader */
uint8_t xtod_nibble(char c) {
  if (c>='0' && c<='9') return c-'0';
  if (c>='A' && c<='F') return c-'A'+10;
  if (c>='a' && c<='f') return c-'a'+10;
return c=0;
}

uint8_t xtod_byte(char c[2]) {
  return (xtod_nibble(c[1]) + (xtod_nibble(c[0]) << 4));
}

PmReturn_t
co_copy(pPmCo_t pco, pPmCo_t *r_pco)
{
    PmReturn_t retval = PM_RET_OK;
    pPmCo_t    pnewco;
    uint8_t   *pchunk;

    /* Allocate a code obj */
    retval = heap_getChunk(sizeof(PmCo_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pnewco = (pPmCo_t)pchunk;

    /* Fill in the CO struct */
    OBJ_SET_TYPE(pnewco, OBJ_TYPE_COB);

    /* Copy fixed size elements */
    pnewco->fixed.co_stacksize   = co_getStacksize(pco);    
    pnewco->fixed.co_argcount    = co_getArgcount(pco);    
    pnewco->fixed.co_flags       = co_getFlags(pco);    
    pnewco->fixed.co_nlocals     = co_getNlocals(pco);    
    pnewco->fixed.co_firstlineno = co_getFirstlineno(pco);    
#ifdef HAVE_CLOSURES
    pnewco->fixed.co_nfreevars   = co_getNfreevars(pco);    
#endif /* HAVE_CLOSURES */

    /* Copy objects */
    retval = obj_copy((pPmObj_t)co_getConsts(pco), (pPmObj_t *)&pnewco->co_consts);
    PM_RETURN_IF_ERROR(retval);
    retval = obj_copy((pPmObj_t)co_getNames(pco), (pPmObj_t *)&pnewco->co_names);
    PM_RETURN_IF_ERROR(retval);
    retval = obj_copy((pPmObj_t)co_getVarNames(pco), (pPmObj_t *)&pnewco->co_varnames);
    PM_RETURN_IF_ERROR(retval);
    retval = obj_copy((pPmObj_t)co_getFilename(pco), (pPmObj_t *)&pnewco->co_filename);
    PM_RETURN_IF_ERROR(retval);
    retval = obj_copy((pPmObj_t)co_getLnotab(pco), (pPmObj_t *)&pnewco->lnotab);
    PM_RETURN_IF_ERROR(retval);
    retval = obj_copy((pPmObj_t)co_getCode(pco), (pPmObj_t *)&pnewco->code);
    PM_RETURN_IF_ERROR(retval);
#ifdef HAVE_CLOSURES
    retval = obj_copy((pPmObj_t)co_getCellvars(pco), (pPmObj_t *)&pnewco->co_cellvars);
    PM_RETURN_IF_ERROR(retval);
#endif /* HAVE_CLOSURES */

    *r_pco = pnewco;
    return retval;
}

PmReturn_t
no_copy(pPmNo_t pno, pPmNo_t *r_pno)
{
    PmReturn_t retval = PM_RET_OK;
    uint8_t *pchunk;

    /* Allocate a code obj */
    retval = heap_getChunk(sizeof(PmNo_t), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    *r_pno = (pPmNo_t)pchunk;
        
    /* Fill in the NO struct */
    OBJ_SET_TYPE(pno, OBJ_TYPE_NOB);
    (*r_pno)->no_argcount = pno->no_argcount;
    (*r_pno)->no_funcindx = pno->no_funcindx;

    return retval;
}

