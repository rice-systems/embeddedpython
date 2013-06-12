/* vm/dict.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __DICT_H__
#define __DICT_H__


/**
 * \file
 * \brief Dict Object Type
 *
 * Dict object type header.
 */


/**
 * Dict
 *
 * Contains ptr to two seglists,
 * one for keys, the other for values;
 * and a length, the number of key/value pairs.
 */
typedef struct PmDict_s
{
    /** object descriptor */
    PmObjDesc_t od;
    /** number of key,value pairs in the dict */
    int16_t length;
    /** ptr to seglist containing keys */
    pSeglist_t d_keys;
    /** ptr to seglist containing values */
    pSeglist_t d_vals;
} PmDict_t,
 *pPmDict_t;


/**
 * Clears the contents of a dict.
 * after this operation, the dict should in the same state
 * as if it were just created using dict_new().
 *
 * @param   pdict ptr to dict to clear.
 * @return  nothing
 */
PmReturn_t dict_clear(pPmDict_t pdict);

/**
 * Gets the value in the dict using the given key.
 *
 * @param   pdict ptr to dict to search
 * @param   pkey ptr to key obj
 * @param   r_pobj Return; addr of ptr to obj
 * @return  Return status
 */
PmReturn_t dict_getItem(pPmDict_t pdict, pPmObj_t pkey, pPmObj_t *r_pobj);

#ifdef HAVE_DEL
/**
 * Removes a key and value from the dict.
 * Throws TypeError if pdict is not a dict.
 * Throws KeyError if pkey does not exist in pdict.
 *
 * @param   pdict Ptr to dict to search
 * @param   pkey Ptr to key obj
 * @return  Return status
 */
PmReturn_t dict_delItem(pPmDict_t pdict, pPmObj_t pkey);
#endif /* HAVE_DEL */

/**
 * Allocates space for a new Dict.
 * Return a pointer to the dict by reference.
 *
 * @param   r_pdict Return; Addr of ptr to dict
 * @return  Return status
 */
PmReturn_t dict_new(pPmDict_t *r_pdict);

/**
 * Sets a value in the dict using the given key.
 *
 * If the dict already contains a matching key, the value is
 * replaced; otherwise the new key,val pair is inserted
 * at the front of the dict (for fast lookup).
 * In the later case, the length of the dict is incremented.
 *
 * @param   pdict ptr to dict in which (key,val) will go
 * @param   pkey ptr to key obj
 * @param   pval ptr to val obj
 * @return  Return status
 */
PmReturn_t dict_setItem(pPmDict_t pdict, pPmObj_t pkey, pPmObj_t pval);

#ifdef HAVE_PRINT
/**
 * Prints out a dict. Uses obj_print() to print elements.
 *
 * @param pobj Object to print.
 * @return Return status
 */
PmReturn_t dict_print(pPmDict_t pdict);
#endif /* HAVE_PRINT */

/**
 * Updates the destination dict with the key,value pairs from the source dict
 *
 * @param   pdestdict ptr to destination dict in which key,val pairs will go
 * @param   psourcedict ptr to source dict which has all key,val pairs to copy
 * @return  Return status
 */
PmReturn_t dict_update(pPmDict_t pdestdict, pPmDict_t psourcedict);

#endif /* __DICT_H__ */
