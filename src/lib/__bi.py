# lib/__bi.py
#
# Provides PyMite's builtins module, __bi.
# The builtins are loaded by the interpreter.
# The user SHOULD NOT import this module directly.
#
# This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import _list, _str, _dict, _set, _thd, _tuple, types, thread

# this should be defined for every class. right now, we're cheating.
__name__ = "(none)"

def me():
    return thread.get_self()

def abs(n):
    return (n, -n)[n < 0]

def _seq2str(s):
    result = ""
    for el in s:
        result += str(el) + ", "
    # remove last comma and space
    return result[0:-2]

def str(n):
    if type(n) == types.IntType:
        return "%d" % n
    elif type(n) == types.FloatType:
        return "%f" % n
    elif type(n) == types.TupleType:
        return "(%s)" % _seq2str(n)
    elif type(n) == types.ListType:
        return "[%s]" % _seq2str(n)
    elif type(n) == types.BooleanType:
        if n:
            return "True"
        else:
            return "False" 
    elif type(n) == types.NoneType:
        return "None"
    else:
        return n

list = _list.list
set = _set.set
tuple = _tuple.tuple

def bool(o):
    if o:
        return True
    else:
        return False

def _varnames(f):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmFunc_t pfunc;
    pPmObj_t  pvarnames;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }
    
    pfunc = (pPmFunc_t) NATIVE_GET_LOCAL(0);

    if (OBJ_GET_TYPE(pfunc) != OBJ_TYPE_FXN)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected function");
        return retval;    
    }

    pvarnames = (pPmObj_t) co_getVarNames(pfunc->f_co);
    NATIVE_SET_TOS(pvarnames);
    return retval;
    """
    pass

def _names(f):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmFunc_t pfunc;
    pPmObj_t  pnames;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }
    
    pfunc = (pPmFunc_t) NATIVE_GET_LOCAL(0);

    if (OBJ_GET_TYPE(pfunc) != OBJ_TYPE_FXN)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected function");
        return retval;    
    }

    pnames = (pPmObj_t) co_getNames(pfunc->f_co);
    NATIVE_SET_TOS(pnames);
    return retval;
    """
    pass

## takes a sequence s and returns a packed tuple with those objects from the sequence
def pack(s):
   r"""__NATIVE__
   PmReturn_t retval = PM_RET_OK;
   pPmObj_t parg;
   pPmPackTuple_t r_ptp;

   parg = NATIVE_GET_LOCAL(0);

   /* If wrong number of args, raise TypeError */
   if (NATIVE_GET_NUM_ARGS() != 1)
   {
       PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
       return retval;
   }

   retval = packtuple_packSetup((pPmTuple_t)parg, &r_ptp);
   PM_RETURN_IF_ERROR(retval);

   NATIVE_SET_TOS((pPmObj_t)r_ptp);
   return retval;
   """
   pass    

## takes a packed tuple and returns a tuple with the same objects from the packed tuple
def unpack(s):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;
    pPmTuple_t r_ptup;

    parg = NATIVE_GET_LOCAL(0);

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    /* If wrong type of argument, raise TypeError */
    if (OBJ_GET_TYPE(parg) != OBJ_TYPE_PTP)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "argument needs to be a packed tuple");
        return retval;
    }

    retval = tuple_copy((pPmTuple_t)parg, &r_ptup);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS((pPmObj_t)r_ptup);
    return retval;    
    """
    pass

def copy(o):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;
    pPmObj_t pobj;
    
    parg = NATIVE_GET_LOCAL(0);

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    retval = obj_copy(parg, &pobj);
    PM_RETURN_IF_ERROR(retval);

    NATIVE_SET_TOS(pobj);
    return retval;
    """
    pass

## returns True if o is able to be packed into a packed tuple and False otherwise
def isPackable(o):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t parg;
    int8_t r_bol;
    pPmObj_t pobj;

    parg = NATIVE_GET_LOCAL(0);

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    retval = obj_isPackable(parg, &r_bol, &pobj);
    PM_RETURN_IF_ERROR(retval);    
    if (r_bol == C_TRUE)
    {
        NATIVE_SET_TOS(PM_TRUE);
    }
    else 
    {
        NATIVE_SET_TOS(PM_FALSE);
    }
    
    return retval;
    """
    pass

HEXDIGITS = '0123456789abcdef'
def hex(i):
    if i < 0:
        i = i*(-1)
        negative = True
    else:
        negative = False

    outstr = ""

    while i:
        outstr = HEXDIGITS[i % 16] + outstr
        i = i >> 4

    if negative:
        return '-0x' + outstr
    else:
        return '0x' + outstr

## in real python max/min can take multiple arguments and has key argument
def max(iterable):
    out = None
    flag = True
    for element in iterable:
        if flag:
            out = element
            flag = False
        if element > out:
            out = element
    return out

def min(iterable):
    out = None
    flag = True
    for element in iterable:
        if flag:
            out = element
            flag = False
        if element < out:
            out = element
    return out

def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True

def any(iterable):
    for element in iterable:
        if element:
            return True
    return False

def cmp(obj1, obj2):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pobj1;
    pPmObj_t pobj2;
    int8_t num;
    pPmObj_t presult;
   
    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "wrong number of arguments");
        return retval;
    }

    pobj1 = NATIVE_GET_LOCAL(0);
    pobj2 = NATIVE_GET_LOCAL(1);

    num = obj_compare(pobj2, pobj1);
    //lib_printf("num: %d\n", num);

    if (num == C_CMP_ERR)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "comparing incompatible types");
        return retval;
    }
    else if (num == C_GT)
    {
        presult = PM_ONE;
    }
    else if (num == C_EQ)
    {
        presult = PM_ZERO;
    }
    else // num == C_LT
    {
        presult = PM_NEGONE;
    }

    NATIVE_SET_TOS(presult);
    return retval;

    """
    pass

def raise_user_ex(n):
    """__NATIVE__
    pPmObj_t pb;
    PmReturn_t retval;

    pb = NATIVE_GET_LOCAL(0);

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* throw the exception */
    PM_RAISE_WITH_OBJ(retval, PM_RET_EX_USER, pb);
    return retval;

    """
    pass

def chr(n):
    """__NATIVE__
    pPmString_t ps;
    pPmObj_t pn;
    int32_t n;
    uint8_t c;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Raise TypeError if arg is not an int */
    pn = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(pn) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Raise ValueError if arg is not int within range(256) */
    n = ((pPmInt_t)pn)->val;
    if ((n < 0) || (n > 255))
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* Create char string from  integer value */
    c = n & 0xff;
    retval = string_new((char const *)&c, 1, &ps);
    NATIVE_SET_TOS((pPmObj_t)ps);
    return retval;
    """
    pass

def dir(space=None):
    return [x for x in _dir(space) if x and x[0] != '_']

def _dir(o):
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t po;
    pPmObj_t pk;
    pPmList_t pl;
    pSeglist_t psl;
    int16_t i;

    /* Use globals if no arg given */
    if (NATIVE_GET_NUM_ARGS() == 0)
    {
        /* Get the globals dict */
        po = (pPmObj_t)NATIVE_GET_PFRAME()->fo_globals;
    }

    /* Otherwise use the given arg */
    else if (NATIVE_GET_NUM_ARGS() == 1)
    {
        po = NATIVE_GET_LOCAL(0);

        /* If object is a function or module, use its attrs dict */
        if ((OBJ_GET_TYPE(po) == OBJ_TYPE_FXN)
            || (OBJ_GET_TYPE(po) == OBJ_TYPE_MOD))
        {
            po = (pPmObj_t)((pPmFunc_t)po)->f_attrs;
        }

#ifdef HAVE_CLASSES
        else if (OBJ_GET_TYPE(po) == OBJ_TYPE_CLO)
        {
            po = (pPmObj_t)((pPmClass_t)po)->cl_attrs;
        }
        else if (OBJ_GET_TYPE(po) == OBJ_TYPE_CLI)
        {
            po = (pPmObj_t)((pPmInstance_t)po)->cli_attrs;
        }
        else if (OBJ_GET_TYPE(po) == OBJ_TYPE_MTH)
        {
            po = (pPmObj_t)((pPmMethod_t)po)->m_attrs;
        }
#endif /* HAVE_CLASSES */

        else if (OBJ_GET_TYPE(po) == OBJ_TYPE_NON)
        {
            po = (pPmObj_t)NATIVE_GET_PFRAME()->fo_back->fo_globals;
        }

        else
        {
            po = C_NULL;
        }
    }

    /* Raise TypeError if wrong number of args */
    else
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    if (po == C_NULL)
    {
        pl = (pPmList_t) PM_NONE;
    }
    else
    {
        /* Create new list */
        retval = list_new(&pl);
        PM_RETURN_IF_ERROR(retval);

        /* Copy dict's keys to the list */
        psl = ((pPmDict_t)po)->d_keys;
        for (i = 0; i < ((pPmDict_t)po)->length; i++)
        {
            retval = seglist_getItem(psl, i, &pk);
            PM_RETURN_IF_ERROR(retval);
            retval = list_append(pl, pk);
            PM_RETURN_IF_ERROR(retval);
        }
    }

    NATIVE_SET_TOS((pPmObj_t)pl);
    return retval;
    """
    pass


#
# Evaluates a given code object (created by Co()).
# Optionally accepts a globals dict as the second parameter
# Optionally accepts a locals dict as the third parameter
#
def eval(co, g, l):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t pco;
    pPmObj_t pfunc;
    pPmObj_t pnewframe;
    pPmObj_t pg = C_NULL;
    pPmObj_t pl = C_NULL;

    /* If wrong number of args, raise TypeError */
    if ((NATIVE_GET_NUM_ARGS() == 0) || (NATIVE_GET_NUM_ARGS() > 3))
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Raise ValueError if first arg is not a Code Object */
    pco = NATIVE_GET_LOCAL(0);
    if (!IS_CODE_OBJ(pco))
    {
        PM_RAISE(retval, PM_RET_EX_VAL);
        return retval;
    }

    /* If 2nd arg exists, raise ValueError if it is not a Dict */
    if (NATIVE_GET_NUM_ARGS() >= 2)
    {
        pg = NATIVE_GET_LOCAL(1);
        if (OBJ_GET_TYPE(pg) != OBJ_TYPE_DIC)
        {
            PM_RAISE(retval, PM_RET_EX_VAL);
            return retval;
        }
    }

    /* If no args are given, use the caller's globals for the function's */
    else
    {
        pg = (pPmObj_t)NATIVE_GET_PFRAME()->fo_globals;
    }

    /* If 3rd arg exists, raise ValueError if it is not a Dict */
    if (NATIVE_GET_NUM_ARGS() >= 3)
    {
        pl = NATIVE_GET_LOCAL(2);
        if (OBJ_GET_TYPE(pl) != OBJ_TYPE_DIC)
        {
            PM_RAISE(retval, PM_RET_EX_VAL);
            return retval;
        }
    }

    /* Create func from code object */
    retval = func_new(pco, pg, &pfunc);
    PM_RETURN_IF_ERROR(retval);

    /* Create frame from module object; globals is set to null */
    retval = frame_new(pfunc, &pnewframe);
    PM_RETURN_IF_ERROR(retval);

    /* TODO: Reclaim pnewframe's attrs dict created in frame_new */
    /*
     * By default use calling frame's attrs as local namespace.
     * This works for ipm because the interactive mode
     * needs a locals namespace that persists across calls to eval()
     */
    ((pPmFrame_t)pnewframe)->fo_locals = NATIVE_GET_PFRAME()->fo_locals;

    /* If 2nd arg exists, use it as the global namespace for the new func */
    if (NATIVE_GET_NUM_ARGS() >= 2)
    {
        ((pPmFrame_t)pnewframe)->fo_globals = (pPmDict_t)pg;

        /* If only globals is given, locals defaults to it */
        ((pPmFrame_t)pnewframe)->fo_locals = (pPmDict_t)pg;
    }

    /* If 3rd arg exists, use it as the local namespace for the new func */
    if (NATIVE_GET_NUM_ARGS() >= 3)
    {
        ((pPmFrame_t)pnewframe)->fo_locals = (pPmDict_t)pl;
    }

    /*
     * Set the fo_back frame so flow returns to eval()'s caller when completed.
     * Set the frame pointer so the new frame is interpreted immediately
     * after this function returns.
     */
    ((pPmFrame_t)pnewframe)->fo_back = NATIVE_GET_PFRAME();
    ((pPmFrame_t)pnewframe)->fo_except = NATIVE_GET_PFRAME();
    NATIVE_GET_PFRAME() = (pPmFrame_t)pnewframe;
    retval = PM_RET_FRAME_SWITCH;

    return retval;
    """
    pass

def filter(f, s):
    return [x for x in s if f(x)]

def globals():
    """__NATIVE__
    pPmObj_t pr = C_NULL;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return calling frame's globals dict  on stack*/
    pr = (pPmObj_t)NATIVE_GET_PFRAME()->fo_globals;
    NATIVE_SET_TOS(pr);

    return PM_RET_OK;
    """
    pass

def address(o):
    """__NATIVE__
    PmReturn_t retval;
    pPmInt_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return object's address as an int on the stack */
    retval = int_new((intptr_t)NATIVE_GET_LOCAL(0), &pr);
    NATIVE_SET_TOS((pPmObj_t)pr);

    return retval;
    """
    pass

# we need some sort of id function
id = address

def len(s):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t ps = C_NULL;
    pPmInt_t pr = C_NULL;
    int16_t len;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get first arg */
    ps = NATIVE_GET_LOCAL(0);

    retval = seq_getLength(ps, &len);
    PM_RETURN_IF_ERROR(retval);

    retval = int_new(len, &pr);

    NATIVE_SET_TOS((pPmObj_t)pr);
    return retval;
    """
    pass

def locals():
    """__NATIVE__
    pPmObj_t pr = C_NULL;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Return calling frame's locals dict on the stack */
    pr = (pPmObj_t)NATIVE_GET_PFRAME()->fo_locals;
    NATIVE_SET_TOS(pr);

    return PM_RET_OK;
    """
    pass

def map(f, s):
    # Allocate the array
    r = [None,] * len(s)

    # Call function f once with each argument in sequence s
    i = 0
    for a in s:
        r[i] = f(a)
        i += 1

    # Return list of results
    return r

def ord(s):
    """__NATIVE__
    pPmObj_t ps;
    pPmInt_t pn;
    int32_t n;
    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ps = NATIVE_GET_LOCAL(0);

    /* Raise TypeError if arg is not string of length 1 */
    if ((OBJ_GET_TYPE(ps) != OBJ_TYPE_STR)
        || (((pPmString_t)ps)->length != 1))

    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get integer value of character */
    n = ((pPmString_t)ps)->val[0];
    retval = int_new(n, &pn);
    NATIVE_SET_TOS((pPmObj_t)pn);
    return retval;
    """
    pass

def float(s):
    """__NATIVE__
    pPmObj_t pf;
    pPmObj_t pn;
    PmReturn_t retval = PM_RET_OK;

    /* figure out what we're doing based on how many arguments we've got */
    if (NATIVE_GET_NUM_ARGS() == 0) {
        pf = C_NULL;
    }
    else if (NATIVE_GET_NUM_ARGS() == 1) {
        pf = NATIVE_GET_LOCAL(0);
    } 
    else {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }
    
    retval = float_fromObj(pf, &pn);
 
    NATIVE_SET_TOS((pPmObj_t)pn);
    return retval;
    """
    pass   

def int(s):
    """__NATIVE__
    pPmObj_t pf, pbase;
    pPmInt_t pn;
    int16_t base = 10;
    PmReturn_t retval;

    /* figure out what we're doing based on how many arguments we've got */
    if (NATIVE_GET_NUM_ARGS() == 0) {
        pf = C_NULL;
    }
    else if (NATIVE_GET_NUM_ARGS() == 1) {
        pf = NATIVE_GET_LOCAL(0);
    } 
    else if (NATIVE_GET_NUM_ARGS() == 2) {
        pf = NATIVE_GET_LOCAL(0);
        pbase = NATIVE_GET_LOCAL(1);

        if ((OBJ_GET_TYPE(pf) != OBJ_TYPE_STR) || (OBJ_GET_TYPE(pbase) != OBJ_TYPE_INT)) {
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
        }

        base = ((pPmInt_t)pbase)->val;
    }
    else {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    retval = int_fromObj(pf, &pn, base);
    NATIVE_SET_TOS((pPmObj_t) pn);

    return retval;
    """
    pass

def pow(x, y):
    return x ** y

def enumerate(l):
    n = 0
    out = []
    for e in l:
        out.append((n, e))
        n += 1
    return out

def xrange(a, b=None, c=None):
    if b == None and c == None:
        start = 0
        stop = a
        step = 1
    elif c == None:
        start = a
        stop = b
        step = 1
    else:
        start = a
        stop = b
        step = c

    if step > 0:
        count = (((stop-1) - start) / step) + 1
    else:
        count = (((stop+1) - start) / step) + 1

    if count < 0:
        count = 0

    if count >= 32768:
        raise_user_ex("resulting range object must have fewer than 32K entries")

    return _xrange(count, start, step)

range = xrange

def _xrange(count, start, step):
    """__NATIVE__
    pPmObj_t pcount;
    pPmObj_t pstart;
    pPmObj_t pstep;

    int16_t count;
    int32_t start, step;

    pPmXrange_t pret;

    PmReturn_t retval;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Raise TypeError if arg is not an int */
    pcount = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(pcount) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    count = ((pPmInt_t)pcount)->val;

    /* Raise TypeError if arg is not an int */
    pstart = NATIVE_GET_LOCAL(1);
    if (OBJ_GET_TYPE(pstart) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    start = ((pPmInt_t)pstart)->val;
    
    /* Raise TypeError if arg is not an int */
    pstep = NATIVE_GET_LOCAL(2);
    if (OBJ_GET_TYPE(pstep) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    step = ((pPmInt_t)pstep)->val;

    /* Create char string from  integer value */
    retval = xrange_new(count, start, step, &pret);
    NATIVE_SET_TOS((pPmObj_t)pret);
    return retval;
    """

def sum(s):
    """__NATIVE__
    pPmObj_t ps;
    pPmObj_t pn;
    pPmObj_t po;
    int32_t n;
    uint16_t len;
    uint16_t i;
    PmReturn_t retval;
#ifdef HAVE_FLOAT
    float f;
    uint8_t usefloat = C_FALSE;
#endif /* HAVE_FLOAT */

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the length of the sequence */
    ps = NATIVE_GET_LOCAL(0);
    if (OBJ_GET_TYPE(ps) == OBJ_TYPE_TUP)
    {
        len = ((pPmTuple_t)ps)->length;
    }
    else if (OBJ_GET_TYPE(ps) == OBJ_TYPE_LST)
    {
        len = ((pPmTuple_t)ps)->length;
    }

    /* Raise TypeError if arg is not a sequence */
    else
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Calculate the sum of the sequence */
    n = 0;
#ifdef HAVE_FLOAT
    f = 0.0;
#endif
    for (i = 0; i < len; i++)
    {
        retval = seq_getSubscript(ps, i, &po);

        if (OBJ_GET_TYPE(po) == OBJ_TYPE_INT)
        {
            /* Add value to sum */
            n += ((pPmInt_t)po)->val;
#ifdef HAVE_FLOAT
            f += (float)((pPmInt_t)po)->val;
#endif /* HAVE_FLOAT */
        }

#ifdef HAVE_FLOAT
        else if (OBJ_GET_TYPE(po) == OBJ_TYPE_FLT)
        {
            /* Add value to sum */
            f += ((pPmFloat_t)po)->val;
            usefloat = C_TRUE;
        }
#endif /* HAVE_FLOAT */

        /* Raise TypeError if item is not an integer */
        else
        {
            PM_RAISE(retval, PM_RET_EX_TYPE);
            return retval;
        }
    }

#ifdef HAVE_FLOAT
    if (usefloat)
    {
        retval = float_new(f, &pn);
    }
    else
#endif /* HAVE_FLOAT */
    {
        retval = int_new(n, (pPmInt_t *)&pn);
    }
    NATIVE_SET_TOS(pn);
    return retval;
    """
    pass

def type(o):
    t = _type(o)
    if t == types._PackTupleType:
        return types.TupleType
    elif t == types._PackCodeType:
        return types.CodeType
    else:
        return t

def _type(o):
    """__NATIVE__
    PmReturn_t retval;
    pPmObj_t po = C_NULL;
    pPmInt_t pr = C_NULL;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get arg */
    po = NATIVE_GET_LOCAL(0);

    /* Create int from type enum */
    retval = int_new(OBJ_GET_TYPE(po), &pr);
    NATIVE_SET_TOS((pPmObj_t)pr);
    return retval;
    """
    pass

#
# Returns True if called within a module being run as the main; False otherwise
#
def ismain():
    """__NATIVE__

    NATIVE_SET_TOS((NATIVE_GET_PFRAME()->fo_isImport) ? PM_FALSE : PM_TRUE);

    return PM_RET_OK;
    """
    pass

