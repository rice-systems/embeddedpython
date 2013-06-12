/* vm/strobj.c
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
#define __FILE_ID__ 0x12


/**
 * \file
 * \brief String Object Type
 *
 * String object type opeartions.
 */

#include "pm.h"

/**
 * Creates a new String obj.
 * If len is positive, copy as many chars as given in the len argument
 *
 * Returns by reference a ptr to String obj.
 *
 * Obtain space for String from the heap.
 * Copy string
 * Leave contents of paddr pointing one byte past end of str.
 *
 *
 * @param   paddr ptr to ptr to null term character array or image.
 * @param   len number of characters to copy from the C character array 
 * @param   n Number of times to replicate the given string argument
 * @param   r_pstring Return by reference; ptr to String obj
 * @return  Return status
 */
PmReturn_t string_create(uint8_t const **paddr, int16_t len, int16_t n, 
                         pPmString_t *r_pstring);



PmReturn_t
string_new(char const *pstr, int16_t len, pPmString_t *r_pstring)
{
    uint8_t const *paddr = (uint8_t const *)pstr;
    return string_create(&paddr, len, 1, r_pstring);
}

PmReturn_t
string_replicate(pPmString_t pstring, int16_t n, pPmString_t *r_pstring)
{
    uint8_t *paddr = pstring->val;
    return string_create((uint8_t const **) &paddr, 
                         pstring->length, n, r_pstring);
}


PmReturn_t
string_create(uint8_t const **paddr, int16_t len, int16_t n, 
              pPmString_t *r_pstring)
{
    PmReturn_t retval = PM_RET_OK;
    pPmString_t pstr = C_NULL;
    uint8_t *pdst = C_NULL;
    uint8_t const *psrc = C_NULL;
    uint8_t *pchunk;

    /* Caller must provide length. */
    C_ASSERT(len >= 0);

    /* Get space for String obj */
    retval = heap_getChunk(sizeof(PmString_t) + (len * n), &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pstr = (pPmString_t)pchunk;

    /* Fill the string obj */
    OBJ_SET_TYPE(pstr, OBJ_TYPE_STR);
    pstr->length = len * n;

    /* Copy C-string into String obj */
    pdst = (uint8_t *)&(pstr->val);
    while (--n >= 0)
    {
        psrc = *paddr;
        memcpy(pdst, psrc, len);
        pdst += len;
    }

    /* Be sure paddr points to one byte past the end of the source string */
    *paddr = psrc;

    /* Zero-pad end of string */
    for (; pdst < (uint8_t *)pstr + OBJ_GET_SIZE(pstr); pdst++)
    {
        *pdst = 0;
    }

    *r_pstring = pstr;

    return PM_RET_OK;
}

int8_t
string_compare(pPmString_t pstr1, pPmString_t pstr2)
{
    uint16_t i; 

    for (i = 0; pstr1->val[i] == pstr2->val[i] && i < pstr1->length && i < pstr2->length; i++)
    {
        /* do nothing */
    }
    
    if (pstr1->length == i && pstr2->length == i) //both pstr1 and pstr2 reached their length
    {
        return C_EQ; //0; str2 == str1
    }
    else if (pstr1->length == i) //pstr1 reached its length, but pstr2 did not
    { 
        return C_GT; //1; str2 > str1
    }
    else if (pstr2->length == i) //pstr2 reached its length, but pstr1 did not
    {
        return C_LT; //-1; str2 < str1
    }
    else //neither pstr1 nor pstr2 reached their length
    {
        int8_t result;
        result = pstr2->val[i] - pstr1->val[i];
        if (result < 0)
        {
            return C_LT; //1; str2 > str1
        }
        else
        {
            return C_GT; //-1; str2 < str1
        }
    }
}

#ifdef HAVE_PRINT
PmReturn_t
string_print(pPmObj_t pstr, uint8_t marshall)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t i;
    uint8_t ch;

    C_ASSERT(pstr != C_NULL);

    /* Ensure string obj */
    if (OBJ_GET_TYPE(pstr) != OBJ_TYPE_STR)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    if (marshall)
    {
        if (-1 == lib_printf("'"))
        {
            PM_RAISE(retval, PM_RET_EX_IO);
            return retval;
        }
    }

    for (i = 0; i < (((pPmString_t)pstr)->length); i++)
    {
        ch = ((pPmString_t)pstr)->val[i];
        if (ch == '\\')
        {
            /* Output an additional backslash to escape it. */
            if (-1 == lib_printf("\\\\"))
            {
                PM_RAISE(retval, PM_RET_EX_IO);
                return retval;
            }
        }
        else if (marshall && (ch < (uint8_t)32 || ch >= (uint8_t)128))
        {
            /* If the marshalled char is not printable, print its hex escape code */
            if (-1 == lib_printf("\\x%2x", ch))
            {
                PM_RAISE(retval, PM_RET_EX_IO);
                return retval;
            }
        }
        else
        {
            /* Simply output character */
            if (-1 == lib_printf("%c", ch))
            {
                PM_RAISE(retval, PM_RET_EX_IO);
                return retval;
            }
        }
    }
    if (marshall)
    {
        if (-1 == lib_printf("'"))
        {
            PM_RAISE(retval, PM_RET_EX_IO);
            return retval;
        }
    }

    return retval;
}
#endif /* HAVE_PRINT */


PmReturn_t
string_concat(pPmString_t pstr1, pPmString_t pstr2, pPmObj_t *r_pstring)
{
    PmReturn_t retval = PM_RET_OK;
    pPmString_t pstr = C_NULL;
    uint8_t *pdst = C_NULL;
    uint8_t const *psrc = C_NULL;
    uint8_t *pchunk;
    uint16_t len;

    /* Create the String obj */
    len = pstr1->length + pstr2->length;
    retval = heap_getChunk(sizeof(PmString_t) + len, &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pstr = (pPmString_t)pchunk;
    OBJ_SET_TYPE(pstr, OBJ_TYPE_STR);
    pstr->length = len;

    /* Concatenate C-strings into String obj and apply null terminator */
    pdst = (uint8_t *)&(pstr->val);
    psrc = (uint8_t const *)&(pstr1->val);
    memcpy(pdst, psrc, pstr1->length);
    pdst += pstr1->length;

    psrc = (uint8_t const *)&(pstr2->val);
    memcpy(pdst, psrc, pstr2->length);
    pdst += pstr2->length;
    
    *pdst = '\0';

    *r_pstring = (pPmObj_t)pstr;
    return PM_RET_OK;
}

/*
 * pseq2 is a tuple or a list, and is insured by the function that calls this (join2)
 * join2 also checks that pstr1 is a string
 */
PmReturn_t
string_join(pPmString_t pstr1, pPmObj_t pseq2, pPmString_t *pstr2)
{
    PmReturn_t retval = PM_RET_OK;
    uint16_t len1; // length of the string (separator)
    int16_t len2; // length of the sequence
    uint16_t total; // length of the returned string (*pstr2)
    int16_t i; // index for while loop
    pPmObj_t next; // next item in pseq2
    int16_t nextlen; // length of next item
    uint8_t *pchunk;
    pPmString_t pstr = C_NULL;
    uint8_t *pdst = C_NULL;
    uint8_t const *psrc = C_NULL;

    len1 = pstr1->length;  
    seq_getLength(pseq2, &len2); 

    i = 0;
    total = 0;

    while (i < len2)
    {
        seq_getSubscript(pseq2, i, &next);
        if (OBJ_GET_TYPE(next) == OBJ_TYPE_STR)
        {
            nextlen = ((pPmString_t)next)->length;
            total += nextlen;
        }
        else
        { 
            /* Raise TypeError if the items in the sequence are not strings */
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong argument type, expected a sequence of strings");
            return retval;
        }
        i++;
    }

    total += (len2-1)*len1; 
    /* len2-1 is the # of times the separator will be placed; len1 is the length of the separator
     * total now is the length of the joined string
     */

    /* Create the String obj */
    retval = heap_getChunk(sizeof(PmString_t) + total, &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pstr = (pPmString_t)pchunk;
    OBJ_SET_TYPE(pstr, OBJ_TYPE_STR);
    pstr->length = total;

     /* Concatenate C-strings into String obj and apply null terminator */
    pdst = (uint8_t *)&(pstr->val);
    for (i = 0; i < len2; i++)
    {
        seq_getSubscript(pseq2, i, &next);
        psrc = (uint8_t const *)&(((pPmString_t)next)->val);
        memcpy(pdst, psrc, ((pPmString_t)next)->length);
        pdst += ((pPmString_t)next)->length;

        if (i < (len2-1))
        {
            psrc = (uint8_t const *)&(pstr1->val);
            memcpy(pdst, psrc, pstr1->length);
            pdst += pstr1->length;
        }
    }
    *pdst = '\0';

    *pstr2 = pstr;
    return retval; //PM_RET_OK;        
}

#ifdef HAVE_SLICING
PmReturn_t
string_slice(pPmString_t pstr1, int16_t start, int16_t end, pPmObj_t *r_pstring)
{
    PmReturn_t retval = PM_RET_OK;
    uint8_t const *psrc = C_NULL;
    uint16_t len;

    len = end - start;
    
    if (len > 0)
    {
        // make a pointer to the start of the data within the 
        // original string
        psrc = (uint8_t const *)&(pstr1->val) + start;

        // call the macro to build the string
        retval = string_new((char const *)psrc, len, (pPmString_t *)r_pstring);
    }
    else
    {
        retval = string_new(C_NULL, 0, (pPmString_t *)r_pstring);
    }

    return retval;
}
#endif /* HAVE_SLICING */

#ifdef HAVE_STRING_FORMAT

#define SIZEOF_SMALLFMT 8

PmReturn_t
string_format(pPmString_t pstr, pPmObj_t parg, pPmObj_t *r_pstring)
{
    PmReturn_t retval;
    uint16_t strsize = 0;
    uint16_t strindex;
    uint8_t *fmtcstr;
    uint8_t smallfmtcstr[SIZEOF_SMALLFMT];
    uint8_t i;
    uint8_t j;
    uint8_t argtupleindex = 0;
    pPmObj_t pobj;
    int snprintretval;
    uint8_t expectedargcount = 0;
    pPmString_t pnewstr;
    uint8_t *pchunk;

    /* Get the first arg */
    pobj = parg;

    /* Calculate the size of the resulting string */
    fmtcstr = pstr->val;
    for (i = 0; i < pstr->length; i++)
    {
        /* Count non-format chars */
        if (fmtcstr[i] != '%') { strsize++; continue; }

        /* If double percents, count one percent */
        if (fmtcstr[++i] == '%') { strsize++; continue; }

        /* Get arg from the tuple */
        if (IS_TUPLE_OBJ(parg))
        {
            retval = tuple_getItem((pPmTuple_t)parg, argtupleindex++, &pobj);
            PM_RETURN_IF_ERROR(retval);
        }

        snprintretval = -1;

        /* Format one arg to get its length */
        smallfmtcstr[0] = '%';
        for(j = 1; (i < pstr->length) && (j < SIZEOF_SMALLFMT); i++)
        {
            smallfmtcstr[j] = fmtcstr[i];
            j++;

            if (fmtcstr[i] == 'd')
            {
                if (OBJ_GET_TYPE(pobj) != OBJ_TYPE_INT)
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    return retval;
                }
                smallfmtcstr[j] = '\0';
                snprintretval = lib_snprintf(C_NULL, 0,
                    (char *)smallfmtcstr, ((pPmInt_t)pobj)->val);
                break;
            }

#ifdef HAVE_FLOAT
            else if (fmtcstr[i] == 'f')
            {
                if (OBJ_GET_TYPE(pobj) != OBJ_TYPE_FLT)
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    return retval;
                }
                smallfmtcstr[j] = '\0';
                snprintretval = lib_snprintf(C_NULL, 0,
                    (char *)smallfmtcstr, ((pPmFloat_t)pobj)->val);
                break;
            }
#endif /* HAVE_FLOAT */

            else if (fmtcstr[i] == 's')
            {
                if (OBJ_GET_TYPE(pobj) != OBJ_TYPE_STR)
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    return retval;
                }
                /* assume the entire string will be printed (and no more) */
                snprintretval = ((pPmString_t)pobj)->length;
                break;
            }
        }

        /* Raise ValueError if the format string was bad */
        if (snprintretval < 0)
        {
            PM_RAISE(retval, PM_RET_EX_VAL);
            return retval;
        }

        expectedargcount++;
        strsize += snprintretval;
    }

    /* TypeError wrong number args */
    if ((!IS_TUPLE_OBJ(parg) && (expectedargcount != 1))
        || (IS_TUPLE_OBJ(parg)
            && (expectedargcount != tuple_getLength((pPmTuple_t)parg))))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Allocate and initialize String obj */
    /* Since PmString_t already has space for one character, this
     * is overprovisioned by a byte for snprintf()'s trailing NULL */
    retval = heap_getChunk(sizeof(PmString_t) + strsize, &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pnewstr = (pPmString_t)pchunk;
    OBJ_SET_TYPE(pnewstr, OBJ_TYPE_STR);
    pnewstr->length = strsize;


    /* Fill contents of String obj */
    strindex = 0;
    argtupleindex = 0;
    pobj = parg;

    for (i = 0; i < pstr->length; i++)
    {
        /* Copy non-format chars */
        if (fmtcstr[i] != '%')
        {
            pnewstr->val[strindex++] = fmtcstr[i];
            continue;
        }

        /* If double percents, copy one percent */
        if (fmtcstr[++i] == '%')
        {
            pnewstr->val[strindex++] = '%';
            continue;
        }

        /* Get arg from the tuple */
        if (IS_TUPLE_OBJ(parg))
        {
            retval = tuple_getItem((pPmTuple_t)parg, argtupleindex++, &pobj);
            PM_RETURN_IF_ERROR(retval);
        }

        snprintretval = -1;

        /* Format one arg to get its length */
        smallfmtcstr[0] = '%';
        for(j = 1; (i < pstr->length) && (j < SIZEOF_SMALLFMT); i++)
        {
            smallfmtcstr[j] = fmtcstr[i];
            j++;

            if (fmtcstr[i] == 'd')
            {
                smallfmtcstr[j] = '\0';
                snprintretval = lib_snprintf((char *) &(pnewstr->val[strindex]), 
                    strsize - strindex + 1,
                    (char *)smallfmtcstr, ((pPmInt_t)pobj)->val);
                break;
            }

#ifdef HAVE_FLOAT
            else if (fmtcstr[i] == 'f')
            {
                smallfmtcstr[j] = '\0';
                snprintretval = lib_snprintf((char *) &(pnewstr->val[strindex]), 
                    strsize - strindex + 1,
                    (char *)smallfmtcstr, ((pPmFloat_t)pobj)->val);
                break;
            }
#endif /* HAVE_FLOAT */

            else if (fmtcstr[i] == 's')
            {
                smallfmtcstr[j] = '\0';
                snprintretval = lib_snprintf((char *) &(pnewstr->val[strindex]), 
                    ((pPmString_t)pobj)->length + 1,
                    (char *)smallfmtcstr, ((pPmString_t)pobj)->val);
                break;
            }
        }

        strindex += snprintretval;
    }
    pnewstr->val[strindex] = '\0';

    *r_pstring = (pPmObj_t)pnewstr;
    return PM_RET_OK;
}
#endif /* HAVE_STRING_FORMAT */

int16_t
string_strstr(pPmString_t haystack, int16_t offset, pPmString_t needle)
{
    int16_t i;

    for (i = offset; i <= (haystack->length - needle->length); i++)
    {
        if (strncmp((const char *)&(haystack->val[i]), (const char *)needle->val, needle->length) == 0)
        {
            return i;
        }
    }

    return -1;
}

PmReturn_t
string_split(pPmString_t ps1, pPmString_t ps2, pPmBoolean_t pb, pPmList_t *pl)
{
    PmReturn_t retval = PM_RET_OK;
    int16_t start_offset, offset;
    uint16_t ps1len, ps2len;
    pPmObj_t ps3;
    uint8_t c;

    start_offset = 0;
    offset = 0;
    ps1len = ps1->length;
    ps2len = ps2->length;

    if (ps2len == 0)
    {
        /* the separator is empty, raise an exception and return none */
        *pl = (pPmList_t)PM_NONE;
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "empty separator");
        return retval;
    }

    retval = list_new(pl);
    PM_RETURN_IF_ERROR(retval);

    while (offset < ps1len)
    {        
        if (pb->val == 0) 
        {
            /* if whitespace is false, search for ps2 */
            offset = string_strstr(ps1, offset, ps2);
        }
        else 
        {
            /* whitespace is true, move offset to first whitespace */
            for (; offset < ps1len; offset++)
            {
                c = ps1->val[offset];
                if ((c == ' ' || c == '\n'|| c == '\t'))
                {
                    break;
                }
            }            
        }

        if (offset == -1)
        {
            /* whitespace, and separator is not found */
            retval = string_slice(ps1, start_offset, ps1len, &ps3);
            PM_RETURN_IF_ERROR(retval);
            retval = list_append(*pl, ps3);
            PM_RETURN_IF_ERROR(retval);
            break;
        }
        else if (pb->val == 0 || start_offset != offset) /* whitespace, or non-empty non-whitespace */
        {
            /* add the string to the list of strings */
            retval = string_slice(ps1, start_offset, offset, &ps3);
            PM_RETURN_IF_ERROR(retval);
            retval = list_append(*pl, ps3);
            PM_RETURN_IF_ERROR(retval);
        }
        
        if (pb->val == 0)
        {
            /* move past the separator so it isn't found again */
            offset += ps2len;
        }
        else 
        {
            /* move past the whitespace */
            c = ps1->val[offset];
            while ((c == ' ' || c == '\n'|| c == '\t'))
            {
                offset++;
                c = ps1->val[offset];
            }
        }

        start_offset = offset;
        if (pb->val == 0) /* whitespace is false */
        {
            if (start_offset == ps1len)
            {
                /* if separator is at the end of the string, add '' to the list of strings */
                retval = string_new(C_NULL, 0, (pPmString_t *)&ps3);
                PM_RETURN_IF_ERROR(retval);
                retval = list_append(*pl, ps3);
                PM_RETURN_IF_ERROR(retval);
                break;
    
            }
        }
    }
    return retval;    
}

