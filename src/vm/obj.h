/* vm/obj.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __OBJ_H__
#define __OBJ_H__


/**
 * \file
 * \brief Object Type
 *
 * Object type header.
 */

/** Object descriptor field constants */
#define OD_MARK_SHIFT 30
#define OD_FREE_SHIFT 31
#define OD_MARK_BIT (uint32_t)(1 << OD_MARK_SHIFT)
#define OD_FREE_BIT (uint32_t)(1 << OD_FREE_SHIFT)
#define OD_SIZE_MASK (uint32_t)(0x003FFF00)
#define OD_SIZE_SHIFT 6
#define OD_TYPE_MASK (uint32_t)(0x000000FF)
#define OD_TYPE_SHIFT 0

#define IS_CODE_OBJ(pobj)  \
    ((OBJ_GET_TYPE(pobj) == OBJ_TYPE_COB) || (OBJ_GET_TYPE(pobj) == OBJ_TYPE_PCO))

#define IS_TUPLE_OBJ(pobj)  \
    ((OBJ_GET_TYPE(pobj) == OBJ_TYPE_TUP) || (OBJ_GET_TYPE(pobj) == OBJ_TYPE_PTP))

/**
 * Gets the free bit of the given object to the given value.
 * If the object is marked free, it is not being used by the VM.
 */
#define OBJ_GET_FREE(pobj) \
    ((((pPmObj_t)pobj)->od >> OD_FREE_SHIFT) & (uint8_t)1)

/**
 * Sets the free bit of the given object to the given value.
 * Setting the free bit means that the object will use the heap descriptor
 * structure instead of the object descriptor structure.
 */
#define OBJ_SET_FREE(pobj, free) \
    do \
    { \
        ((pPmObj_t)pobj)->od = ((uint8_t)free) \
                               ? ((pPmObj_t)pobj)->od | OD_FREE_BIT \
                               : ((pPmObj_t)pobj)->od & ~OD_FREE_BIT;\
    } \
    while (0)

/*
 * #99: od_size bits are shifted because size is a scaled value
 * True size is always a multiple of 4, so the lower two bits are ignored
 * and two more significant bits are gained.
 */
/**
 * Gets the size of the chunk in bytes.
 * Tests whether the object is free as that determines whether the chunk is
 * using an object descriptor or a heap descriptor.  Heap descriptors have
 * a larger size field and use a different bit mask than object descriptors.
 */
#define OBJ_GET_SIZE(pobj) \
    ((((pPmObj_t)pobj)->od & OD_SIZE_MASK) >> OD_SIZE_SHIFT)

/**
 * Sets the size of the chunk in bytes.
 * Tests whether the object is free as that determines whether the chunk is
 * using an object descriptor or a heap descriptor.  Heap descriptors have
 * a larger size field and use a different bit mask than object descriptors.
 */
#define OBJ_SET_SIZE(pobj, size) \
    do \
    { \
        ((pPmObj_t)pobj)->od &= ~OD_SIZE_MASK; \
        ((pPmObj_t)pobj)->od |= (((size) << OD_SIZE_SHIFT) & OD_SIZE_MASK); \
    } \
    while (0)

/**
 * Gets the type of the object
 * This MUST NOT be called on objects that are free.
 */
#define OBJ_GET_TYPE(pobj) \
    (((((pPmObj_t)pobj)->od) & OD_TYPE_MASK) >> OD_TYPE_SHIFT)

/**
 * Sets the type of the object
 * This MUST NOT be called on objects that are free.
 */
#define OBJ_SET_TYPE(pobj, type) \
    do \
    { \
        ((pPmObj_t)pobj)->od &= ~OD_TYPE_MASK; \
        ((pPmObj_t)pobj)->od |= (((type) << OD_TYPE_SHIFT) & OD_TYPE_MASK); \
    } \
    while (0)


/**
 * Object type enum
 *
 * These values go in the od_type fields of the obj descriptor.
 * Be sure these values correspond to those in the image creator
 * tool.
 * The hashable types are grouped together for convenience.
 *
 * WARNING: od_type must be at most 5 bits! (must be < 0x20)
 */
typedef enum PmType_e
{
    OBJ_TYPE_HASHABLE_MIN = 0x00,

    OBJ_TYPE_PACKABLE_MIN = 0x00,

    /** None */
    OBJ_TYPE_NON = 0x00,

    /** Signed integer */
    OBJ_TYPE_INT = 0x01,

    /** Floating point 32b */
    OBJ_TYPE_FLT = 0x02,

    /** String */
    OBJ_TYPE_STR = 0x03,

    /** Tuple (immutable sequence) */
    OBJ_TYPE_TUP = 0x04,

    /** Packed tuple */
    OBJ_TYPE_PTP = 0x05,

    /** Boolean object */
    OBJ_TYPE_BOL = 0x06,

    /** type 0x07 is reserved **/

    /** Code obj */
    OBJ_TYPE_COB = 0x08,
    
    /** Packed code object */
    OBJ_TYPE_PCO = 0x09,

    /* All types after this are not packable */
    OBJ_TYPE_PACKABLE_MAX = 0x14,

    /** Module obj */
    OBJ_TYPE_MOD = 0x15,

    /** Class obj */
    OBJ_TYPE_CLO = 0x16,

    /** Function obj (callable) */
    OBJ_TYPE_FXN = 0x17,

    /** Class instance */
    OBJ_TYPE_CLI = 0x18,

    /** Native function object */
    OBJ_TYPE_NOB = 0x19,

    /* Foreign function object */
    OBJ_TYPE_FOR = 0x1A,

    /** Thread */
    OBJ_TYPE_THR = 0x1B,

    /** type 0x1C is reserved **/
    
    /** Method object */
    OBJ_TYPE_MTH = 0x1D,
    
    /* All types after this are not hashable */
    OBJ_TYPE_HASHABLE_MAX = 0x27,

    /** List (mutable sequence) */
    OBJ_TYPE_LST = 0x28,

    /** Dictionary (hash table) */
    OBJ_TYPE_DIC = 0x29,

    /** xrange */
    OBJ_TYPE_XRA = 0x2A,

    /** Set */
    OBJ_TYPE_SET = 0x2B,

    /** Any */
    OBJ_TYPE_ANY = 0x2C,

    /* All types after this are not accessible to the user */
    OBJ_TYPE_ACCESSIBLE_MAX = 0x33,

    /** Frame type */
    OBJ_TYPE_FRM = 0x34,

    /** Block type (for,while,try,etc) */
    OBJ_TYPE_BLK = 0x35,

    /** Segment (within a seglist) */
    OBJ_TYPE_SEG = 0x36,

    /** Seglist */
    OBJ_TYPE_SGL = 0x37,

    /** Sequence iterator */
    OBJ_TYPE_SQI = 0x38,

    /** type 0x3e is reserved **/

    /** Profiler arrays */
    OBJ_TYPE_PRO = 0x3F,
} PmType_t, *pPmType_t;

// update this as new objects are added
#define MAX_OBJ 0x3F

/**
 * Object Descriptor
 *
 * All active PyMite "objects" must have this at the top of their struct.
 * (CodeObj, Frame, Dict, List, Tuple, etc.).
 *
 * The following is a diagram of the object descriptor:
 *
 *              MSb           LSb
 *               7 6 5 4 3 2 1 0
 *     pchunk-> +-+-+-+-+-+-+-+-+     S := Size of the chunk (2 LSbs dropped)
 *              |     S[9:2]    |     F := Free bit
 *              +-+-+---------+-+     M := GC Mark bit
 *              |F|M|    T    |S|     T := Object type (PyMite specific)
 *              +-+-+---------+-+
 *              | object data   |
 *              ...           ...
 *              | end data      |     Theoretical min size == 2
 *              +---------------+     Effective min size == 8
 *                                    (due to pmHeapDesc_t)
 *
 * Macros are used to get and set field values.
 * Using macros eliminates declaring bit fields which fails on some compilers.
 */
typedef uint32_t PmObjDesc_t,
 *pPmObjDesc_t;

/**
 * Object
 *
 * The abstract empty object type for PyMite.
 */
typedef struct PmObj_s
{
    /** Object descriptor */
    PmObjDesc_t od;
} PmObj_t,
 *pPmObj_t;

/** Boolean object */
typedef struct PmBoolean_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Boolean value */
    int32_t val;
}
PmBoolean_t, *pPmBoolean_t;


/**
 * Finds the boolean value of the given object.
 *
 * @param   pobj Ptr to object to test.
 * @return  Nonzero value if object is False.
 */
int8_t obj_isFalse(pPmObj_t pobj);

/**
 * Returns the boolean true if the item is in the object
 *
 * @param   pobj Ptr to container object
 * @param   pitem Ptr to item
 */
PmReturn_t obj_isIn(pPmObj_t pobj, pPmObj_t pitem);

/**
 * Compares two objects for equality.
 *
 * @param   pobj1 Ptr to first object.
 * @param   pobj2 Ptr to second object.
 * @return  C_EQ if the items are equivalent, C_NEQ otherwise.
 */
int8_t obj_isEqual(pPmObj_t pobj1, pPmObj_t pobj2);

/**
 * Compares two objects for ordering.
 *
 * @param   pobj1 Ptr to first object.
 * @param   pobj2 Ptr to second object.
 * @return  C_EQ if the items are equivalent, C_GT if pobj2 > pobj1, C_LT otherwise.
 */
int8_t obj_compare(pPmObj_t pobj1, pPmObj_t pobj2);

/**
 * Copies pobj and returns a pointer to a new object
 *
 * @param  pobj Ptr to object to be copied
 * @param  r_pobj returned Object
 * @return Return status
 */
PmReturn_t obj_copy(pPmObj_t pobj, pPmObj_t *r_pobj);

/**
 * Checks pobj and returns True or False based off whether pobj is able to be
 * packed into a packtuple. If pobj is a tuple, checks recursively.
 *
 * @param  pobj Ptr to object to be checked
 * @param  r_bol C_TRUE if can be put in packtuple, C_FALSE otherwise
 * @param  r_pobj The first object reached that is unable to be packed, C_NULL if 
 *                there is no object (C_TRUE)
 * @return Return status
 */
PmReturn_t obj_isPackable(pPmObj_t pobj, int8_t *r_bol, pPmObj_t *r_pobj);

/**
 * Print an object, thereby using objects helpers.
 *
 * @param   pobj Ptr to object for printing.
 * @param   marshallString Only has influence on the way strings are printed.
 *                         If 0, just output the string bytewise. Otherwise,
 *                         surround with single quotes and escape unprintable
 *                         characters.
 * @return  Return status
 */
PmReturn_t obj_print(pPmObj_t pobj, uint8_t marshallString);

#endif /* __OBJ_H__ */
