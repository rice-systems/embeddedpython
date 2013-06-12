/* vm/float.c
 *
 * This file is Copyright 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __FLOAT_H__
#define __FLOAT_H__


/**
 * \file
 * \brief Float Object Type
 *
 * Float object type header.
 */


/**
 * Float obj
 *
 * 32b floating point number
 */
typedef struct PmFloat_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Float value */
    float val;
} PmFloat_t, *pPmFloat_t;


#ifdef HAVE_FLOAT

// convert an arbitrary python object into a float
PmReturn_t float_fromObj(pPmObj_t pf, pPmObj_t *r_pf);

/**
 * Creates a new Float object
 *
 * @param   f Value to assign float (signed 32-bit).
 * @param   r_pint Return by ref, ptr to new float
 * @return  Return status
 */
PmReturn_t float_new(float f, pPmObj_t *r_pf);

/**
 * Implements the UNARY_NEGATIVE bcode.
 *
 * Creates a new float with a value that is the negative of the given float.
 *
 * @param   pobj Pointer to target object
 * @param   r_pint Return by ref, ptr to float
 * @return  Return status
 */
PmReturn_t float_negative(pPmObj_t pf, pPmObj_t *r_pf);

/**
 * Returns by reference a float that is x op y.
 *
 * @param px The float left-hand argument
 * @param py The float right-hand argument
 * @param r_pn The return value of x op y
 * @param op The operator (+,-,*,/ and power)
 * @return Return status
 */
PmReturn_t float_op(pPmObj_t px, pPmObj_t py, pPmObj_t *r_pn, int8_t op);

/**
 * Compares two objects, one of type flt, the other of bool, flt, or int, for ordering.
 *
 * @param   pobj1 Ptr to first object.
 * @param   pobj2 Ptr to second object.
 * @return C_EQ if the items are equivalent, C_GT if pobj2 > pobj1, C_LT otherwise.
 */
int8_t float_compare(pPmObj_t pobj1, pPmObj_t pobj2);

#ifdef HAVE_PRINT
/**
 * Sends out a float object.
 * The number is preceded with a "-" when necessary.
 *
 * @param pObj Ptr to float object
 * @return Return status
 */
PmReturn_t float_print(pPmObj_t pf);

/*
 * Given an object of a numeric type (OBJ_TYPE_FLT, OBJ_TYPE_INT, or 
 * OBJ_TYPE_BOL) returns a float representation of that object's value.
 * Raises a TypeError if the object passed in was not of numeric type.
 */
PmReturn_t float_getval(pPmObj_t num, pPmObj_t *val);

#endif /* HAVE_PRINT */

#endif /* HAVE_FLOAT */

#endif /* __FLOAT_H__ */
