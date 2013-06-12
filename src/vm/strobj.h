/* vm/strobj.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __STRING_H__
#define __STRING_H__


/**
 * \file
 * \brief String Object Type
 *
 * String object type header.
 */



/***************************************************************
 * Types
 **************************************************************/

/**
 * String obj
 *
 * Null terminated array of chars.
 */
typedef struct PmString_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Length of string */
    uint16_t length;

    /**
     * Null-term char array
     *
     * Use length 1 here so that string-alloc function can use
     * "sizeof(PmString_t) + len" and there will be room for the null-term
     */
    uint8_t val[1];
} PmString_t,
 *pPmString_t;


/***************************************************************
 * Prototypes
 **************************************************************/

/**
 * Creates String object from character array in RAM which may contain
 * embedded null characters.
 *
 * @param pstr pointer to source string
 * @param len length of source string
 * @param r_pstring Return arg; addr of ptr to string
 */
PmReturn_t
string_new(char const *pstr, int16_t len, pPmString_t *r_pstring);

/**
 * Creates String object by replicating an existing string, n times
 *
 * @param pstring pointer to source string
 * @param n number of times to replicate the source string
 * @param r_pstring Return arg; addr of ptr to string
 */

PmReturn_t
string_replicate(pPmString_t pstring, int16_t n, pPmString_t *r_pstring);

/**
 * Compares two String objects for ordering.
 *
 * @param   pstr1 Ptr to first string
 * @param   pstr2 Ptr to second string
 * @return  C_EQ if the strings are equivalent, C_GT if pstr2 > pstr1, C_LT otherwise
 */
int8_t string_compare(pPmString_t pstr1, pPmString_t pstr2);

#ifdef HAVE_PRINT
/**
 * Sends out a string object bytewise. Escaping and framing is configurable
 * via marshall.
 *
 * @param pobj Ptr to string object
 * @param marshall If 0, print out string as is. Otherwise escape unprintable
 *                 characters and surround string with single quotes.
 * @return Return status
 */
PmReturn_t string_print(pPmObj_t pstr, uint8_t marshall);
#endif /* HAVE_PRINT */

/**
 * Returns a new string object that is the joining of the strings in pseq2 with the 
 * separator pstr1.
 * @param pstr1 separator string
 * @param pseq2 sequence of strings
 * @param pstr2 Return arg; ptr to new string object
 * @return Return status
 */
PmReturn_t string_join(pPmString_t pstr1, pPmObj_t pseq2, pPmString_t *pstr2);

/**
 * Returns a new string object that is the concatenation 
 * of the two given strings.
 *
 * @param pstr1 First source string
 * @param pstr2 Second source string
 * @param r_pstring Return arg; ptr to new string object
 * @return Return status
 */
PmReturn_t
string_concat(pPmString_t pstr1, pPmString_t pstr2, pPmObj_t *r_pstring);

#ifdef HAVE_SLICING
/**
 * Slice a string
 */
PmReturn_t
string_slice(pPmString_t pstr1, int16_t start, int16_t end, pPmObj_t *r_pstring);
#endif /* HAVE_SLICING */

#ifdef HAVE_STRING_FORMAT
/**
 * Returns a new string object that is created from the given format string
 * and the argument(s).
 *
 * @param pstr Format string object
 * @param parg Single argument or tuple of arguments
 * @param r_pstring Return arg; ptr to new string object
 * @return Return status
 */
PmReturn_t string_format(pPmString_t pstr, pPmObj_t parg, pPmObj_t *r_pstring);
#endif /* HAVE_STRING_FORMAT */

/**
 * Returns the index of needle in haystack or -1 if needle is not found
 * starting the search from the given offset in haystack.
 *
 * @param haystack String to find needle in
 * @param offset Index to start searching haystack for needle
 * @param needle String to find in haystack
 * @return Index of needle in haystack
 */
int16_t string_strstr(pPmString_t haystack, int16_t offset, pPmString_t needle);

/**
 * Returns a list of the split strings.
 *
 * @param ps1 String to be split
 * @param ps2 String to split with
 * @param pb Boolean representing whitespace as on or off
 * @param pl List to hold the split strings
 * @return Return status
 */
PmReturn_t string_split(pPmString_t ps1, pPmString_t ps2, pPmBoolean_t pb, pPmList_t *pl);

#endif /* __STRING_H__ */
