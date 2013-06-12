# tools/build/autowrap/autowrap_backend.py
#
# generates output of autowrapped functions
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.


from clean import Cleaner
import re
import os

# any preamble that needs to be there?
#HEADER = "# autowrapped file"
HEADER = open('stm32/header.txt').read()

# from here are things specific to the VM. this should need to be changed
PREAMBLE = r"""def %s():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;"""

FOOTER = r"""
    return retval;
    '''
    pass

    """

ARGCHECK = r"""
    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != %d)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }"""

CONVERT_NUM_ARG = r"""
    p%(num)d = NATIVE_GET_LOCAL(%(num)d);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p%(num)d) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    %(cname)s = ((pPmInt_t)p%(num)d)->val;"""
    
CONVERT_PM_ARG = r"""
    p%(num)d = NATIVE_GET_LOCAL(%(num)d);

    /* If arg is not an $(obj_type_name)s, raise TypeError */
    if (OBJ_GET_TYPE(p%(num)d) != %(obj_type_macro)s)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE, "expected %(obj_type_macro)s";
        return retval;
    }

    %(cname)s = p%(num)d"""
    
CONVERT_PMOBJECT_ARG = r"""
    p%(num)d = NATIVE_GET_LOCAL(%(num)d);

    %(cname)s = p%(num)d"""

CONVERT_BOOL_ARG = r"""
    p%(num)d = NATIVE_GET_LOCAL(%(num)d);

    /* If arg is not an int, raise TypeError */
    if (p%(num)d == PM_TRUE) {
        %(cname)s = true;
    } else if (p%(num)d == PM_FALSE) {
        %(cname)s = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }"""

RESULT_HEADER = r"""
    pPmObj_t pret;
    %s cret;"""

STORE_RESULT_NUM = r"""
    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);"""
    
STORE_RESULT_PM = r"""
    NATIVE_SET_TOS((pPmObj_t) cret);"""
    
STORE_RESULT_BOOL = r"""
    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }"""

CONVERT_ARG = {'unsigned long': CONVERT_NUM_ARG,
               'int': CONVERT_NUM_ARG,
               'unsigned char': CONVERT_NUM_ARG,
               'unsigned short': CONVERT_NUM_ARG,
               'u64': CONVERT_NUM_ARG,
               'u32': CONVERT_NUM_ARG,
               'u16': CONVERT_NUM_ARG,
               'u8': CONVERT_NUM_ARG,
               'tBoolean': CONVERT_BOOL_ARG,
               '_Bool': CONVERT_BOOL_ARG}

STORE_RESULT = {'unsigned long': STORE_RESULT_NUM,
                'long': STORE_RESULT_NUM,
                'int': STORE_RESULT_NUM,
                'u32': STORE_RESULT_NUM,
                'u16': STORE_RESULT_NUM,
                'u8': STORE_RESULT_NUM,
                'tBoolean': STORE_RESULT_BOOL,
                '_Bool': STORE_RESULT_BOOL}

def convert_arg(arg_type, arg_name, n):
    if arg_type == 'pPmObj_t':
        print CONVERT_PMOBJECT_ARG % {'num':n, 'cname':arg_name}
    if 'pPm' in arg_type:
        print CONVERT_PMOBJECT_ARG % {'num':n, 
                                      'cname':arg_name,
                                      'obj_type_macro': name_to_macro(arg_type)}
    else:
        try:
            print CONVERT_ARG[arg_type] % {'num':n, 'cname':arg_name}
        except KeyError:
            raise AutowrapError, "can't convert argument of type %s" % arg_type

def store_result(ret_type):
    if 'pPm' in ret_type:
        print STORE_RESULT_PM
    try:
        print STORE_RESULT[ret_type]
    except KeyError:
        raise AutowrapError, "can't convert return type %s" % ret_type

class AutowrapError(Exception):
    pass

class AutowrapBackend(object):
    def __init__(self, fn):
        self.fn = fn
        self.cleaner = Cleaner(fn)

        name = fn.split('.')[0]

        print HEADER.format(CAPNAME=name.upper(), NAME=name)

    def comment(self, text):
        print "\n#", text

    def define(self, name, val):
        name = self.cleaner.clean(name)
        print "%s = %s" % (name, val)

    def function(self, ret_type, name, args):
        c_args = ", ".join([t[1] for t in args])

        # strip out the file name at the start of the function
        short_name = self.cleaner.clean(name)
        print PREAMBLE % (short_name)
        
        # print the python object list
        local_c = ["p%d" % p for p in range(len(args))];
        print "    pPmObj_t %s;" % ", ".join(local_c)
        
        # print the C argument list
        for (dtype, argname) in args:
            print '    %s %s;' % (dtype, argname)
            
        # prepare a place for the result
        returns_value = (ret_type != 'void')
        if returns_value:
            print RESULT_HEADER % ret_type

        # make sure we got the right number of arguments
        print ARGCHECK % len(args)

        # convert all the arguments
        for n, (arg_type, arg_name) in enumerate(args):
            convert_arg(arg_type, arg_name, n)

        # make the actual function call
        if returns_value:
            print "\n    cret = %s(%s);" % (name, c_args)
        else:
            print "\n    %s(%s);\n" % (name, c_args)
        
        # collect the result
        if returns_value:
            store_result(ret_type)
        else:
            print "    NATIVE_SET_TOS(PM_NONE);"

        print FOOTER

