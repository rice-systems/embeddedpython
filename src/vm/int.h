/* vm/int.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __INT_H__
#define __INT_H__


/**
 * \file
 * \brief Integer Object Type
 *
 * Integer object type header.
 */

/**
 * Integer obj
 *
 * 32b signed integer
 */
typedef struct PmInt_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Integer value */
    int32_t val;
} PmInt_t,
 *pPmInt_t;


/**
 * Creates a new Integer object
 *
 * @param   val Value to assign int (signed 32-bit).
 * @param   r_pint Return by ref, ptr to new int
 * @return  Return status
 */
PmReturn_t int_new(int32_t val, pPmInt_t *r_pint);

// convert an arbitrary object into an int
PmReturn_t int_fromObj(pPmObj_t pf, pPmInt_t *pn, int16_t base);

/**
 * Implements the UNARY_POSITIVE bcode.
 *
 * Creates a new int with the same value as the given int.
 *
 * @param   pobj Pointer to integer object
 * @param   r_pint Return by reference, ptr to int
 * @return  Return status
 */
PmReturn_t int_positive(pPmInt_t pobj, pPmInt_t *r_pint);

/**
 * Implements the UNARY_NEGATIVE bcode.
 *
 * Creates a new int with a value that is the negative of the given int.
 *
 * @param   pobj Pointer to target object
 * @param   r_pint Return by ref, ptr to int
 * @return  Return status
 */
PmReturn_t int_negative(pPmInt_t pobj, pPmInt_t *r_pint);

/**
 * Implements the UNARY_INVERT bcode.
 *
 * Creates a new int with a value that is
 * the bitwise inversion of the given int.
 *
 * @param   pobj Pointer to integer to invert
 * @param   r_pint Return by reference; new integer
 * @return  Return status
 */
PmReturn_t int_bitInvert(pPmInt_t pobj, pPmInt_t *r_pint);

#ifdef HAVE_PRINT
/**
 * Sends out an integer object in decimal notation with MSB first.
 * The number is preceded with a "-" when necessary.
 *
 * @param pObj Ptr to int object
 * @return Return status
 */
PmReturn_t int_print(pPmInt_t pint);
#endif /* HAVE_PRINT */

/**
 * Returns by reference an integer that is x raised to the power of y.
 *
 * @param px The integer base
 * @param py The integer exponent
 * @param r_pn Return by reference; New integer with value of x ** y
 * @return Return status
 */
PmReturn_t int_pow(pPmInt_t px, pPmInt_t py, pPmInt_t *r_pn);

/**
 * Compares two objects (int or bool) for ordering.
 *
 * @param   pobj1 Ptr to first object.
 * @param   pobj2 Ptr to second object.
 * @return  C_EQ if the items are equivalent, C_GT if pobj2 > pobj1, C_LT otherwise.
 */
int8_t int_compare(pPmObj_t pobj1, pPmObj_t pobj2);

#endif /* __INT_H__ */
