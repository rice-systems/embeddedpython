# lib/_str.py
#
# Defines string methods.
#
# This file is Copyright 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.


"""__NATIVE__
#include <stdlib.h>
#include <string.h>
"""

__name__ = "string"

class _Autobox:
    def join(self, l):
        return join(self.obj, l)

    def split(self, s=None):
        return split(self.obj, s)

    def count(self, s):
        return count(self.obj, s)

    def find(self, s):
        return find(self.obj, s)

    def strip(self):
        return strip(self.obj)


digits = "0123456789"
hexdigits = "0123456789abcdefABCDEF"
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def strip(s):
    return split(s)[0]

def join(separator, l):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg0;
    pPmObj_t parg1;
    pPmString_t presult;
    
    /* Raise TypeError if it's not a list or tuple or wrong number of args. */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    parg0 = NATIVE_GET_LOCAL(0);
    parg1 = NATIVE_GET_LOCAL(1);

    if ((!IS_TUPLE_OBJ(parg1)) && (OBJ_GET_TYPE(parg1) != OBJ_TYPE_LST)
        && (OBJ_GET_TYPE(parg0) != OBJ_TYPE_STR))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong argument type");
        return retval;
    }

    retval= string_join((pPmString_t)parg0, parg1, &presult);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)presult);
    return retval;
    """
    pass

def split(l, s=None):
    if (s==None):
        s = " "
        whitespace = True
    else:
        whitespace = False

    return _split(l, s, whitespace)

def _split(instring, sep, mode):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmList_t pl;

    pPmString_t ps1;
    pPmString_t ps2;

    pPmObj_t pb;

    /* Raise TypeError if it's not a string or wrong number of args, */
    ps1 = (pPmString_t) NATIVE_GET_LOCAL(0);
    ps2 = (pPmString_t) NATIVE_GET_LOCAL(1);
    pb = NATIVE_GET_LOCAL(2);
    if ((OBJ_GET_TYPE(ps1) != OBJ_TYPE_STR) || (NATIVE_GET_NUM_ARGS() != 3)
        || (OBJ_GET_TYPE(ps2) != OBJ_TYPE_STR))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    retval = string_split(ps1, ps2, (pPmBoolean_t)pb, &pl);

    NATIVE_SET_TOS((pPmObj_t) pl);
    return retval;
    '''
    pass

#
# Returns the number of occurrences of substring s2 in string s1.
# WARNING: Does not match Python's behavior if s1 contains a null character.
#
def count(s1, s2):
    """__NATIVE__
    pPmString_t ps1;
    pPmString_t ps2;
    uint16_t ps1len;
    uint16_t ps2len;
    uint16_t n;
    int16_t offset;
    pPmInt_t pn;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a string or wrong number of args, */
    ps1 = (pPmString_t)NATIVE_GET_LOCAL(0);
    ps2 = (pPmString_t)NATIVE_GET_LOCAL(1);
    if ((OBJ_GET_TYPE(ps1) != OBJ_TYPE_STR) || (NATIVE_GET_NUM_ARGS() != 2)
        || (OBJ_GET_TYPE(ps2) != OBJ_TYPE_STR))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ps1len = ps1->length;
    ps2len = ps2->length;
    n = 0;
    offset = 0;
    
    if (ps2len == 0)
    {
        /* separator is empty so skip while loop */
        offset = ps1len;
        /* this is what real python does */
        n = ps1len + 1;
    }

    while (offset < ps1len)
    {
        offset = string_strstr(ps1, offset, ps2);
        if (offset == -1)
        {
            break;
        }
        n++;
        offset += ps2len;
    }

    retval = int_new(n, &pn);

    NATIVE_SET_TOS((pPmObj_t)pn);

    return retval;
    """
    pass


#
# Returns the lowest index in s1 where substring s2 is found or -1 on failure.
# WARNING: Does not accept optional start,end arguments.
#
def find(s1, s2):
    """__NATIVE__
    pPmString_t ps1;
    pPmString_t ps2;
    int32_t n;
    pPmInt_t pn;
    PmReturn_t retval = PM_RET_OK;

    /* Raise TypeError if it's not a string or wrong number of args, */
    ps1 = (pPmString_t)NATIVE_GET_LOCAL(0);
    ps2 = (pPmString_t)NATIVE_GET_LOCAL(1);
    if ((OBJ_GET_TYPE(ps1) != OBJ_TYPE_STR) || (NATIVE_GET_NUM_ARGS() != 2)
        || (OBJ_GET_TYPE(ps2) != OBJ_TYPE_STR))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    n = string_strstr(ps1, 0, ps2);
    retval = int_new(n, &pn);

    NATIVE_SET_TOS((pPmObj_t)pn);

    return retval;
    """
    pass


# :mode=c:
