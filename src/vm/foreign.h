/* vm/foreign.h
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#ifndef __FOREIGN_H__
#define __FOREIGN_H__

#ifdef HAVE_FFI

/**
 * Foreign function
 *
 */
typedef struct PmForeign_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Set length */
    uint16_t num_params;

    // and the indirection length...
    uint8_t indirection_length;

    // pointer to function of arbitrary signature
    // (yes, I know this is non-conforming)
    union fn
    {
        uint32_t *fn_pointer;
        uint8_t path[4];
    } fn;
    
    /** array of argument types */
    uint8_t params[1];

} __attribute__((packed)) PmForeign_t,
 *pPmForeign_t;

/**
 * Allocates a new foreign function object.
 *
 * @param   r_pobj Return; addr of ptr to obj
 * @return  Return status
 */
PmReturn_t foreign_new(uint16_t num_params, pPmForeign_t *r_pobj);

// copy a foreign function. allocate memory for the target.
PmReturn_t foreign_copy(pPmForeign_t psrc, pPmForeign_t *pdst);

#ifdef HAVE_PRINT
/**
 * Prints out a foreign function pointer. Uses obj_print() to print elements.
 *
 * @param   pforeign Foreign object to print
 * @return  Return status
 */
PmReturn_t foreign_print(pPmForeign_t pforeign);
#endif /* HAVE_PRINT */

// calls a foreign function
PmReturn_t foreign_call(pPmForeign_t pcallable, pPmTuple_t args, pPmObj_t *r_pobj);

#endif // HAVE_FFI
#endif /* __FOREIGN_H__ */

