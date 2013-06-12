#!/usr/bin/env python2.7
#
# tools/user/pmImgCreator.py
#
# This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

"""
PyMite Image Creator
====================

Converts Python source files to a PyMite code image library.
Performs code filtering to ensure it will run in PyMite.
Formats the image as a raw binary file or a C file
containing a byte array.

16- and 32-bit values are in LITTLE ENDIAN order.
This matches both Python and the AVR compiler's access to EEPROM.

The order of the images in the output is undetermined.

If the Python source contains a native code declaration
and '--native-file=filename" is specified, the native code
is formatted as C functions and an array of functions and output
to the given filename.  When native functions are present, the user
should specify where the native functions should be placed-- in the
standard library or the user library--using the argument -s or -u,
respectively.
"""

## @file
#  @copybrief pmImgCreator

## @package pmImgCreator
#  @brief PyMite Image Creator
#
#  See the source docstring for more details.

__usage__ = """USAGE:
    pmImgCreator.py [-b|c] [-s|u] [OPTIONS] -o imgfilename file0.py [files...]

    -b      Generates a raw binary file of the image
    -c      Generates a C file of the image (default)

    -s      Place native functions in the PyMite standard library (default)
    -u      Place native functions in the user library

    OPTIONS:
    --native-file=filename  If specified, pmImgCreator will write a C source
                            file with native functions from the python files.
    --memspace=ram|flash    Sets the memory space in which the image will be
                            placed (default is "ram")
    """


import exceptions, string, sys, types, os, time, getopt, struct
import pmTypes

import toolchain

# make sure we're running on a valid version of python
if not sys.version[:3] in ['2.7']:
    raise SystemError, "Must be running Python 2.7"

#
# IMPORTANT: The following dict MUST reflect the HAVE_* items in pmfeatures.h.
# If the item is defined in pmfeatures.h, the corresponding dict value should
# be True; False otherwise.
#
PM_FEATURES = {
    "HAVE_PRINT": True, # This flag currently has no effect in this file
    "HAVE_GC": True, # This flag currently has no effect in this file
    "HAVE_FLOAT": True,
    "HAVE_DEL": True,
    "HAVE_IMPORTS": True,
    "HAVE_ASSERT": True,
    "HAVE_DEFAULTARGS": True,
    "HAVE_VARARGS": True,
    "HAVE_REPLICATION": True, # This flag currently has no effect in this file
    "HAVE_CLASSES": True,
    "HAVE_GENERATORS": True,
    "HAVE_CLOSURES": True,
}


################################################################
# CONSTANTS
################################################################

# Exit error codes (from /usr/include/sysexits.h)
EX_USAGE = 64

# remove documentation string from const pool
REMOVE_DOC_STR = True

# Pm obj descriptor type constants
# Must match PmType_e in pm.h
OBJ_TYPE_NON = pmTypes.NoneType       # None
OBJ_TYPE_INT = pmTypes.IntType        # Signed integer
OBJ_TYPE_FLT = pmTypes.FloatType      # Floating point 32b
OBJ_TYPE_STR = pmTypes.StringType     # String
OBJ_TYPE_TUP = pmTypes.TupleType      # Tuple (static sequence)
OBJ_TYPE_PTP = pmTypes._PackTupleType # Packed Tuple
OBJ_TYPE_MOD = pmTypes.ModuleType     # Module obj
OBJ_TYPE_CLO = pmTypes.ClassType      # Class obj
OBJ_TYPE_FXN = pmTypes.FunctionType   # Funtion obj
OBJ_TYPE_COB = pmTypes.CodeType       # Code obj
OBJ_TYPE_NOB = pmTypes.NativeCodeType # Native func obj
OBJ_TYPE_FOR = pmTypes.ForeignType    # FFI
OBJ_TYPE_PCO = pmTypes._PackCodeType  # Packed Code obj

# All types after this never appear in an image

# Number of bytes in a native image (constant)
NATIVE_IMG_SIZE = 4

# Maximum number of objs in a tuple
MAX_TUPLE_LEN = 253

# Maximum number of chars in a string (XXX bytes vs UTF-8 chars?)
# This is arbitrary, really limited by uint16_t len field of PmString_t
MAX_STRING_LEN = 4096

# Maximum size of a packed tuple
# This is fixed by the uint16_t size filed of PmPackTuple_t
MAX_TUPLE_SIZE = 65535

# Maximum number of chars in a code img
# Not sure what limits this
#MAX_IMG_LEN = 32767
MAX_IMG_LEN = 66863

MAX_FFI_INDIRECTION_LENGTH = 4

# Masks for co_flags (from Python's code.h)
CO_OPTIMIZED = 0x0001
CO_NEWLOCALS = 0x0002
CO_VARARGS = 0x0004
CO_VARKEYWORDS = 0x0008
CO_NESTED = 0x0010
CO_GENERATOR = 0x0020
CO_NOFREE = 0x0040

# String used to ID a native method
NATIVE_INDICATOR = "__NATIVE__"
NATIVE_INDICATOR_LENGTH = len(NATIVE_INDICATOR)

# String name of function table variable
NATIVE_TABLE_NAME = {"std": "std_nat_fxn_table",
                     "usr": "usr_nat_fxn_table"
                    }

# String name to prefix all native functions
NATIVE_FUNC_PREFIX = "nat_"

# maximum number of locals a native func can have
NATIVE_NUM_LOCALS = 8

# Issue #51: In Python 2.5, the module identifier changed from '?' to '<module>'
if float(sys.version[:3]) < 2.5:
    MODULE_IDENTIFIER = "?"
else:
    MODULE_IDENTIFIER = "<module>"

# PyMite's unimplemented bytecodes (from Python 2.0 through 2.5)
UNIMPLEMENTED_BCODES = [
    # "SLICE+1", "SLICE+2", "SLICE+3",
    "STORE_SLICE+0", "STORE_SLICE+1", "STORE_SLICE+2", "STORE_SLICE+3",
    "DELETE_SLICE+0", "DELETE_SLICE+1", "DELETE_SLICE+2", "DELETE_SLICE+3",
    "PRINT_ITEM_TO", "PRINT_NEWLINE_TO",
    "WITH_CLEANUP", "SETUP_WITH",
    "EXEC_STMT",
    "END_FINALLY",
    "SETUP_EXCEPT", "SETUP_FINALLY",
    "BUILD_SLICE",
    "CALL_FUNCTION_VAR", "CALL_FUNCTION_KW", "CALL_FUNCTION_VAR_KW",
    "EXTENDED_ARG",
    ]

if not PM_FEATURES["HAVE_DEL"]:
    UNIMPLEMENTED_BCODES.extend([
        "DELETE_SUBSCR",
        "DELETE_NAME",
        "DELETE_GLOBAL",
        "DELETE_ATTR",
        "DELETE_FAST",
        ])

if not PM_FEATURES["HAVE_IMPORTS"]:
    UNIMPLEMENTED_BCODES.extend([
        "IMPORT_STAR",
        "IMPORT_FROM",
        ])

if not PM_FEATURES["HAVE_ASSERT"]:
    UNIMPLEMENTED_BCODES.extend([
        "RAISE_VARARGS",
        ])

if not PM_FEATURES["HAVE_CLASSES"]:
    UNIMPLEMENTED_BCODES.extend([
        "BUILD_CLASS",
        ])

# #207: Add support for the yield keyword
if not PM_FEATURES["HAVE_GENERATORS"]:
    UNIMPLEMENTED_BCODES.extend([
        "YIELD_VALUE",
        ])

# #213: Add support for Python 2.6 bytecodes.
# The *_TRUE_DIVIDE bytecodes require support for float type
if not PM_FEATURES["HAVE_FLOAT"]:
    UNIMPLEMENTED_BCODES.extend([
        "BINARY_TRUE_DIVIDE",
        "INPLACE_TRUE_DIVIDE",
        ])

# #152: Byte to append after the last image in the list
IMG_LIST_TERMINATOR = "\xFF"

# #256: Add support for decorators
if not PM_FEATURES["HAVE_CLOSURES"]:
    UNIMPLEMENTED_BCODES.extend([
        "MAKE_CLOSURE",
        "LOAD_CLOSURE",
        "LOAD_DEREF",
        "STORE_DEREF",
        ])

FFI_TYPE_CODES = {
    'u8':100,
    's8':101,
    'u16':102,
    's16':103,
    'u32':104,
    's32':105,
    'bool':106,
    'void':200}

FFI_INDIRECT_MARKER = "indirect "

################################################################
# GLOBALS
################################################################


def byte_hex(s):
    return " ".join(["%02x" % ord(c) for c in s])


################################################################
# CLASS
################################################################

class NoNativeFileException(Exception):
    pass

class PmImgCreator:

    def __init__(self,):
        self.reinit()

        # keep track of how much we're sinking into BC and strings
        self.strings_len = 0
        self.all_strings = []
        self.num_strings = 0
        self.bc_len = 0
        self.debug_len = 0

    def reinit(self):
        self.formatFromExt = {".c": self.format_img_as_c,
                              ".bin": self.format_img_as_bin,
                             }

        # bcode to mnemonic conversion (sparse list of strings)
        bcodes = toolchain.dis.opname[:]

        # remove invalid bcodes
        for i in range(len(bcodes)):
            if bcodes[i][0] == '<':
                bcodes[i] = None

        # remove unimplmented bcodes
        for bcname in UNIMPLEMENTED_BCODES:
            if bcname in bcodes:
                i = bcodes.index(bcname)
                bcodes[i] = None

        # set class variables
        self.bcodes = bcodes

        # function renames
        self._U8_to_str = chr
        self._str_to_U8 = ord

    def set_options(self,
                    outfn,
                    imgtype,
                    imgtarget,
                    memspace,
                    nativeFilename,
                    infiles,
                   ):
        self.outfn = outfn
        self.imgtype = imgtype
        self.imgtarget = imgtarget
        self.memspace = memspace
        self.nativeFilename = nativeFilename
        self.infiles = infiles

################################################################
# CONVERSION FUNCTIONS
################################################################

    def convert_files(self,):
        """Attempts to convert all source files.
        Creates a dict whose keys are the filenames
        and values are the code object string.
        """
        # init image dict
        imgs = {"imgs": [], "fns": []}

        # init module table and native table
        self.nativemods = []
        self.nativetable = []

        # if creating usr lib, create placeholder in 0th index
        if self.imgtarget == "usr":
            self.nativetable.append((NATIVE_FUNC_PREFIX + "placeholder_func",
                                    "\n    /*\n"
                                    "     * Use placeholder because an index \n"
                                    "     * value of zero denotes the stdlib.\n"
                                    "     * This function should not be called.\n"
                                    "     */\n"
                                    "    PmReturn_t retval;\n"
                                    "    PM_RAISE(retval, PM_RET_EX_SYS);\n"
                                    "    return retval;\n"
                                   , None, 0))
            self.nfcount = 1
        else:
            self.nfcount = 0

        # for each src file, convert and format
        total_size = 0

        for fn in self.infiles:
            # set toolchain type based on file extension
            if fn.endswith('py'):
                toolchain.set_mode('python')
            else:
                print "unsupported file type:", fn
                continue
            
            # now, reset us.
            self.reinit()

            # try to compile and convert the file
            source = open(fn).read()
            
            # convert line endings
            source = source.replace('\r\n', '\n')

            # make sure there's nothing absurd like a tab in the file
            if '\t' in source:
                print "ERROR: tabs not allowed in source files"
                sys.exit(1)

            co = toolchain.compile(source, fn, 'exec')
            imgs["fns"].append(fn)
            img = self.co_to_img(co)
            imgs["imgs"].append(img)
            
            total_size += len(img)
            print " %s: %.1f kB" % (fn, len(img)/1000.0)

        # collect the summary info
        # the above info is counted as strings, so let's not double count
        strings_len = self.strings_len - self.bc_len - self.debug_len
        other_len = total_size - self.strings_len
        self.summary = (self.bc_len, self.debug_len, strings_len, other_len)

        print " --Summary--"
        print "  bytecodes    : %.1f kB" % (self.bc_len/1000.0)
        print "  debug info:  : %.1f kB" % (self.debug_len/1000.0)
        print "  misc strings : %.1f kB" % (strings_len/1000.0)
        print "  other        : %.1f kB" % (other_len/1000.0)
        print " -----------"
        print "  total size   : %.1f kB" % (total_size/1000.0)
        print " -----------"

        #print "longest string:"
        #self.all_strings.sort(key=lambda x: len(x), reverse=True)
        #for s in self.all_strings: print s
        
        # Append null terminator to list of images
        imgs["fns"].append("img-list-terminator")
        imgs["imgs"].append(IMG_LIST_TERMINATOR)

        self.imgDict = imgs
        return


    def _str_to_U16(self, s):
        """Convert two bytes from a sequence to a 16-bit word.

        The bytes are expected in little endian order.
        LSB first.
        """

        return self._str_to_U8(s[0]) | (self._str_to_U8(s[1]) << 8)


    def _U16_to_str(self, w):
        """Convert the 16-bit word, w, to a string of two bytes.

        The 2 byte string is in little endian order.
        DOES NOT INSERT TYPE BYTE.
        """

        return self._U8_to_str(w & 0xff) + \
               self._U8_to_str((w >> 8) & 0xff)


    def _U32_to_str(self, w):
        """Convert the 16-bit word, w, to a string of two bytes.

        The 2 byte string is in little endian order.
        DOES NOT INSERT TYPE BYTE.
        """

        return self._U8_to_str(w & 0xff) + \
               self._U8_to_str((w >> 8) & 0xff) + \
               self._U8_to_str((w >> 16) & 0xff) + \
               self._U8_to_str((w >> 24) & 0xff)


    def _create_od(self, objtype, objlen):
        """Create a 4 byte object descriptor"""
        # round up to 4B alignment
        if objlen & 0x3:
            objlen += 4
        # Length in 4B words
        objlen = objlen >> 2
        # Actual descriptor
        od  = self._U8_to_str(objtype)
        od += self._U8_to_str(objlen & 0xff) 
        od += self._U8_to_str((objlen >> 8) & 0x3f)
        od += self._U8_to_str(0)
        return od

    def _pad(self, imgstr):
        """Add zeros to pad imgstr to multiple of 4B"""
        n = len(imgstr) & 0x3
        while n:
            imgstr += chr(0)
            n = (n + 1) & 0x3
        return imgstr

    def _none_to_img(self):
        """Create a NONE object"""
        return self._create_od(OBJ_TYPE_NON, 4)

    def _int_to_img(self, i):
        """Convert the integer, i, to a p14p int object"""
        # Object Descriptor
        imgstr  = self._create_od(OBJ_TYPE_INT, 8)
        # Int
        imgstr += self._U8_to_str(i & 0xff)
        imgstr += self._U8_to_str((i >>  8) & 0xff)
        imgstr += self._U8_to_str((i >> 16) & 0xff)
        imgstr += self._U8_to_str((i >> 24) & 0xff)
        
        return imgstr

    def _float_to_img(self, f):
        """Convert the float, f, to a p14p float object"""
        # Object Descriptor
        imgstr  = self._create_od(OBJ_TYPE_FLT, 8)
        # Float
        imgstr += struct.pack("<f", f)
        return imgstr

    def _str_to_img(self, s):
        """Convert the string, s, to a p14p string object"""
        # ensure string is not too long
        assert len(s) <= MAX_STRING_LEN
        # marker, object descriptor, string length, string itself
        objlen = len(s) + 7 # object descriptor (4B), length (2B), NULL (1B)
        # Object descriptor
        imgstr  = self._create_od(OBJ_TYPE_STR, objlen)
        # Length and string
        imgstr += self._U16_to_str(len(s)) + s
        # NULL
        imgstr += chr(0)
        # Pad to 4B boundary
        imgstr = self._pad(imgstr)

        self.all_strings.append(s)
        self.strings_len += len(imgstr)
        self.num_strings += 1

        return imgstr

    def _for_to_img(self, s):
        """Convert the string, s, to a p14p foreign function object"""

        try:
            header, parts = s.split(':')
            parts = parts.split('/')

            # if it's an indirect path...
            if parts[0].startswith(FFI_INDIRECT_MARKER):
                path = parts[0][len(FFI_INDIRECT_MARKER):].split('.')
                path = [int(step) for step in path]
            else:
                path = None
                fn_pointer = int(parts[0], 16)

            args = [FFI_TYPE_CODES[p] for p in parts[1:]]

        except ValueError, IndexError:
            raise
            raise ValueError, "malformed FFI entry: %s" % s

        # TODO: check maximum argcount

        # object descriptor (4B), length (2B), indirection path length (1b),
        # function pointer (4B)
        objlen = 11 + len(args)

        # Object descriptor
        imgstr  = self._create_od(OBJ_TYPE_FOR, objlen)
        
        # Length
        imgstr += self._U16_to_str(len(args))

        if path:
            # indirection length
            imgstr += self._U8_to_str(len(path))

            if len(path) > MAX_FFI_INDIRECTION_LENGTH:
                raise ValueError, "ffi indirection path too long"

            # insert a maximum of four path elements
            for step in path:
                imgstr += self._U8_to_str(step)

            for step in range(MAX_FFI_INDIRECTION_LENGTH-len(path)):
                imgstr += self._U8_to_str(0)

        else:
            # function pointer
            imgstr += self._U8_to_str(0)
            imgstr += self._U32_to_str(fn_pointer)

        # all the args
        for arg in args:
            imgstr += chr(arg)
        
        # Pad to 4B boundary
        imgstr = self._pad(imgstr)

        # print byte_hex(imgstr)

        return imgstr

    def _seq_to_img(self, seq):
        """Convert a Python sequence to a PyMite image.

        The sequence is converted to a tuple of objects.
        This handles both co_consts and co_names.
        This is recursive to handle tuples in the const pool.
        Return string shows type in the leading byte.
        """

        # OPT
        _U8_to_str = self._U8_to_str

        # ensure tuple fits within limits
        assert len(seq) <= MAX_TUPLE_LEN

        imgstr = ""

        # iterate through the sequence of objects
        for i in range(len(seq)):
            obj = seq[i]
            objtype = type(obj)

            # if it is a string
            if objtype == types.StringType:
                if obj.startswith('__FFI__'):
                    imgstr += self._for_to_img(obj)
                else:
                    imgstr += self._str_to_img(obj)

            # if it is an integer
            elif objtype in [types.IntType, types.LongType]:
                # marker, int (little endian)
                imgstr += self._int_to_img(obj)

            # if it is a code object
            elif objtype == types.CodeType:
                #determine if it's native or regular
                if (len(obj.co_consts) > 0 and
                    (type(obj.co_consts[0]) == types.StringType) and
                    (obj.co_consts[0][0:NATIVE_INDICATOR_LENGTH] ==
                    NATIVE_INDICATOR)):
                    imgstr += self.no_to_img(obj)
                else:
                    imgstr += self.co_to_img(obj)

            # if it is a tuple
            elif objtype == types.TupleType:
                imgstr += self._seq_to_img(obj)

            # if it is a list, convert to tuple
            elif objtype == types.ListType:
                imgstr += self._seq_to_img(obj)

            # if it is None
            elif objtype == types.NoneType:
                # marker, none (0)
                imgstr += self._none_to_img()

            # if it is a float
            elif objtype == types.FloatType and PM_FEATURES["HAVE_FLOAT"]:
                imgstr += self._float_to_img(obj)

            # other type?
            else:
                raise exceptions.NotImplementedError(
                          "Unhandled type %s." % objtype)

        assert len(imgstr) <= MAX_TUPLE_SIZE

        # Prepend appropriate header
        header  = self._create_od(OBJ_TYPE_PTP, len(imgstr) + 8)
        header += self._U16_to_str(len(seq))
        header += self._U16_to_str(len(imgstr))

        imgstr = header + imgstr
        imgstr = self._pad(imgstr)

        return imgstr


    def co_to_img(self, co):
        """Convert a Python code object to a PyMite image.

        The code image is relocatable and goes in the device's
        memory. Return string shows type in the leading byte.
        """

        # filter code object elements
        consts, names, varnames, code, nativecode = self._filter_co(co, False)

        # Fixed size elements
        fixed = ""

        # skip co_type and size
        # co_stacksize
        fixed += self._U8_to_str(co.co_stacksize)
        # co_argcount
        fixed += self._U8_to_str(co.co_argcount)
        # co_flags
        fixed += self._U8_to_str(co.co_flags & 0xFF)
        # co_nlocals
        fixed += self._U8_to_str(co.co_nlocals)
        # co_firstlineno
        fixed += self._U16_to_str(co.co_firstlineno)
        # #256: Add support for closures
        # nfreevars
        if PM_FEATURES["HAVE_CLOSURES"]:
            fixed += self._U8_to_str(len(co.co_freevars))
        else:
            fixed += chr(0xaa) # pad byte
        fixed += chr(0x55) # pad byte


        # Variable length objects
        varylist = [names, varnames, consts, co.co_filename, co.co_lnotab, code]
        varylist_nodebug = [names, consts, code]

        # #256: Add support for closures
        if PM_FEATURES["HAVE_CLOSURES"]:
            # Lookup the index of the cellvar name in co_varnames; -1 if not in
            l = [-1,] * len(co.co_cellvars)
            for i,name in enumerate(co.co_cellvars):
                if name in co.co_varnames:
                    l[i] = list(co.co_varnames).index(name)
            varylist.append(tuple(l))
        
        # count the debug info contained therein
        # TWB measured the overhead of including this, per cob to be 28 bytes
        # above and beyond the size of their constituents. since excluding them
        # would also exclude their headers, let's account all 28 bytes to the 
        # debugging info

        local_debug_len = len(co.co_filename) + len(co.co_lnotab) + 28
        self.debug_len += local_debug_len

        # nothing we can do about the headers here.
        self.bc_len += len(code)
        
        vary = self._seq_to_img(tuple(varylist))

        imgstr = fixed + vary

        # Create object descriptor, prepend it, and pad the string
        od = self._create_od(OBJ_TYPE_PCO, len(imgstr)+4)
        imgstr = od + imgstr
        imgstr = self._pad(imgstr)
        
        # ensure string length fits within S16 type
        assert len(imgstr) <= MAX_IMG_LEN

        return imgstr


    def no_to_img(self, co):
        """Convert a native code object to a PyMite image.

        The native image is relocatable and goes in the device's
        memory. Return string shows type in the leading byte.
        """

        # filter code object elements
        consts, names, varnames, code, nativecode = self._filter_co(co, True)

        # Object descriptor
        imgstr  = self._create_od(OBJ_TYPE_NOB, 8)
        
        # argcount
        imgstr += self._U8_to_str(co.co_argcount)

        # padding
        imgstr += chr(0)

        # Function Index
        imgstr += code

        # ensure string length fits within S16 type
        assert len(imgstr) <= MAX_IMG_LEN

        return imgstr


################################################################
# FILTER FUNCTION
################################################################

    def _filter_co(self, co, native):
        """Run the Python code obj, co, through various filters.

        Ensure it is compliant with PyMite restrictions.

        Consts filter:
            Ensure num consts is less than 256.
            Replace __doc__ with None if present.

        Flags filter:
            Check co_flags for flags that indicate an unsupported feature
            Supported flags: CO_NOFREE, CO_OPTIMIZED, CO_NEWLOCALS, CO_NESTED,
            Unsupported flags: CO_VARKEYWORDS
            Conditionally supported flags: CO_GENERATOR if HAVE_GENERATORS, 
                                           CO_VARARGS if HAVE_VARARGS

        Native code filter:
            If this function has a native indicator,
            extract the native code from the doc string
            and clear the doc string.
            Ensure num args is less or equal to
            NATIVE_NUM_LOCALS.

        Names/varnames filter:
            Ensure num names is less than 256.
            If co_name is the module identifier replace it with
            the trimmed module name
            otherwise just append the name to co_name.

        Bcode filter:
            Raise NotImplementedError for an invalid bcode.

        If all is well, return the filtered consts list,
        names list, code string and native code.
        """

        ## General filter
        # ensure values fit within S8 type size
        assert len(co.co_consts) < 128, "too many constants."
        assert len(co.co_names) < 128, "too many names."
        assert len(co.co_varnames) < 128, "too many local names."
        assert co.co_argcount < 128, "too many arguments."
        assert co.co_stacksize < 128, "too large of a stack."
        assert co.co_nlocals < 128, "too many local variables."

        # make consts a list so a single element can be modified
        consts = list(co.co_consts)

        # Check co_flags
        unsupported_flags = CO_VARKEYWORDS
        if not PM_FEATURES["HAVE_GENERATORS"]:
            unsupported_flags |= CO_GENERATOR
        if not PM_FEATURES["HAVE_VARARGS"]:
            unsupported_flags |= CO_VARARGS
        if native:
            unsupported_flags |= CO_VARARGS
        assert co.co_flags & unsupported_flags == 0,\
            "Unsupported code identified by co_flags (%s)." % hex(co.co_flags)

        # get trimmed src file name and module name
        fn = os.path.basename(co.co_filename)
        mn = os.path.splitext(fn)[0]

        # init native code
        nativecode = None

        ## Bcode filter
        # bcode string
        s = co.co_code
        # filtered code string
        code = ""
        # iterate through the string
        lno = 0
        i = 0
        len_s = len(s)
        while i < len_s:

            #get char
            c = ord(s[i])

            #ensure no illegal bytecodes are present
            if self.bcodes[c] == None:
                raise NotImplementedError(
                        "Illegal bytecode (%d/%s/%s) "
                        "comes at offset %d in file %s." %
                        (c, hex(c), toolchain.dis.opname[c],
                         i, co.co_filename))

            #if simple bcode, copy one byte
            if c < toolchain.dis.HAVE_ARGUMENT:
                code += s[i]
                i += 1

            #else copy three bytes
            else:

                # Raise error if default arguments exist and are not configured
                if (((not PM_FEATURES["HAVE_DEFAULTARGS"]) or native)
                    and c == toolchain.dis.opmap["MAKE_FUNCTION"]
                    and self._str_to_U16(s[i+1:i+3]) > 0):

                    raise NotImplementedError(
                            "Bytecode (%d/%s/%s) not configured "
                            "to support default arguments; "
                            "comes at offset %d in file %s." %
                            (c, hex(c), toolchain.dis.opname[c], i, co.co_filename))

                # Otherwise, copy the code (3 bytes)
                code += s[i:i+3]
                i += 3

        # if the first const is a String,
        if (len(consts) > 0 and type(consts[0]) == types.StringType):

            ## Native code filter
            # if this CO is intended to be a native func.
            if (consts[0][:NATIVE_INDICATOR_LENGTH] ==
                NATIVE_INDICATOR):

                if not self.nativeFilename:
                    raise NoNativeFileException

                # ensure num args is less or equal
                # to NATIVE_NUM_LOCALS
                assert co.co_nlocals <= NATIVE_NUM_LOCALS

                # extract native code and clear doc string
                nativecode = consts[0][NATIVE_INDICATOR_LENGTH:]
                consts[0] = None

                # If this co is a module
                # Issue #28: Module root must keep its bytecode
                if co.co_name == MODULE_IDENTIFIER:
                    self.nativemods.append((co.co_filename, nativecode))

                # Else this co is a function;
                # replace code with native table index
                else:
                    # stdlib code gets a positive index
                    if self.imgtarget == "std":
                        code = self._U16_to_str(len(self.nativetable))
                    # usr code gets a negative index
                    else:
                        code = self._U16_to_str(-len(self.nativetable))

                    # native function name is
                    # "nat_<modname>_<pyfuncname>".
                    # append (nat func name, nat code) to table
                    self.nativetable.append(
                        ("%s%02d_%s_%s"
                         % (NATIVE_FUNC_PREFIX, self.nfcount, mn, co.co_name),
                         nativecode, co.co_filename, co.co_firstlineno))
                    self.nfcount += 1

            ## Consts filter
            # if want to remove __doc__ string
            # WARNING: this heuristic is not always accurate
            elif (REMOVE_DOC_STR and len(co.co_names) > 0
                  and co.co_names[0] == "__doc__"):
                consts[0] = None

        ## Names filter
        names = list(co.co_names)

        # Remove __doc__ name if requested
        if REMOVE_DOC_STR and len(names) > 0 and names[0] == "__doc__":
            names[0] = ''

        # if co_name is the module identifier change it to module name
        if co.co_name == MODULE_IDENTIFIER:
            names.append(mn)
        # else use unmodified co_name
        else:
            names.append(co.co_name)

        ## Varnames filter
        varnames = list(co.co_varnames)

        return consts, names, varnames, code, nativecode


################################################################
# IMAGE WRITING FUNCTIONS
################################################################

    def write_image_file(self,):
        """Writes an image file
        """
        fmtfxn = self.formatFromExt[self.imgtype]
        f = open(self.outfn, 'wb')
        f.write(fmtfxn())
        f.close()

    def write_native_file(self,):
        """Writes native functions if filename was given
        """
        if not self.nativeFilename:
            return
        f = open(self.nativeFilename, 'wb')
        f.write(self.format_native_table())
        f.close()


    def format_img_as_bin(self,):
        """format_img_as_bin() --> string

        Write image bytes to raw binary string.
        The resulting string is suitable to write to a file.
        """

        # no reformatting necessary, join all object images
        return string.join(self.imgDict["imgs"], "")


    def format_img_as_c(self,):
        """format_img_as_c() --> string

        Format image bytes to a string that is a C byte array.
        The C byte array can be located in RAM
        or program memory.  The byte array is named lib_img.
        """

        # list of filenames
        fns = self.imgDict["fns"]
        imgs = self.imgDict["imgs"]

        # create intro
        fileBuff = []
        fileBuff.append("/**\n"
                        " * PyMite library image file.\n"
                        " *\n"
                        " * Automatically created from:\n"
                        " * \t%s\n"
                        " * by pmImgCreator.py on\n"
                        " * %s.\n"
                        " * \n"
                        " * Byte count: %d\n"
                        " * \n"
                        " * Selected memspace type: %s\n"
                        " * \n"
                        " * DO NOT EDIT THIS FILE.\n"
                        " * ANY CHANGES WILL BE LOST.\n"
                        " */\n\n"
                        % (string.join(fns, "\n *\t"),
                           time.ctime(time.time()),
                           len(string.join(imgs, "")),
                           self.memspace.upper()
                          )
                       )
        fileBuff.append("/* Place the image into %s */\n"
                        "#ifdef __cplusplus\n"
                        "extern\n"
                        "#endif\n"
                        "unsigned char const\n"
                        % self.memspace.upper()
                       )

        if self.memspace.lower() == "flash":
            fileBuff.append("#if defined(__AVR__)\n"
                            "__attribute__((progmem))\n"
                            "#endif\n"
                           )

        fileBuff.append("%slib_img[] =\n"
                        "{\n"
                        % (self.imgtarget)
                       )
        
        fileBuff.append("// stats summary:%s\n" % \
            "/".join([self.outfn] + [str(i) for i in self.summary]))

        # for each src file, convert and format
        i = 0
        for fn in fns:

            # get img string for this file
            img = imgs[i]
            i += 1

            # print all bytes
            fileBuff.append("\n\n/* %s */" % fn)
            j = 0
            while j < len(img):
                if (j % 8) == 0:
                    fileBuff.append("\n    ")
                fileBuff.append("0x%02X, " % ord(img[j]))
                j += 1

        # finish off array
        fileBuff.append("\n};\n")

        return string.join(fileBuff, "")


    def format_native_table(self,):
        """format_native_table() --> string

        Format native table to a C file containing
        native functions and a function table.
        """
        # create intro
        fileBuff = []
        fileBuff.append("#undef __FILE_ID__\n"
                        "#define __FILE_ID__ 0x0A\n"
                        "/**\n"
                        " * PyMite %s native function file\n"
                        " *\n"
                        " * automatically created by pmImgCreator.py\n"
                        " * on %s\n"
                        " *\n"
                        " * DO NOT EDIT THIS FILE.\n"
                        " * ANY CHANGES WILL BE LOST.\n"
                        " *\n"
                        " * @file    %s\n"
                        " */\n\n"
                        "#define __IN_LIBNATIVE_C__\n"
                        "#include \"pm.h\"\n\n"
                        % (self.imgtarget,
                           time.ctime(time.time()),
                           self.nativeFilename
                          )
                       )

        # module-level native sections (for #include headers)
        for (modname, modstr) in self.nativemods:
            fileBuff.append("/* From: %s */%s\n" % (modname, modstr))

        # Create prototypes for each native function
        fileBuff.append("/* Native function prototypes */\n\n");
        for (funcname, funcstr, fname, firstline) in self.nativetable:
            fileBuff.append("PmReturn_t %s(pPmFrame_t *ppframe, int8_t numlocals, pPmObj_t *r_pobj);\n"
                            % (funcname))            

        fileBuff.append("\n\n/* Native functions */\n\n");

        # for each entry create fxn
        for (funcname, funcstr, fname, firstline) in self.nativetable:


            fileBuff.append("PmReturn_t\n"
                            "%s(pPmFrame_t *ppframe, int8_t numlocals, pPmObj_t *r_pobj)\n"
                            "{\n" % funcname)

            # write out the first line number right before the source
            if fname:
                fname = '"%s"' % fname
                fileBuff.append("#line %d %s\n" % (firstline+1, fname))

            fileBuff.append("%s\n"
                            "}\n\n" % funcstr)

        # create fxn table
        fileBuff.append("/* native function lookup table */\n"
                        "typedef PmReturn_t (* pNatFxn)(pPmFrame_t *, int8_t, pPmObj_t *);\n\n"
                        "const pNatFxn %s[] =\n"
                        "{\n" % (NATIVE_TABLE_NAME[self.imgtarget]))

        # put all native funcs in the table
        for (funcname, funcstr, _, _) in self.nativetable:
            fileBuff.append("    %s,\n" % funcname)
        fileBuff.append("};\n")

        return string.join(fileBuff, "")


################################################################
# MAIN
################################################################

def parse_cmdline():
    """Parses the command line for options.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "bcsuo:",
                                   ["memspace=", "native-file="])
    except:
        print __usage__
        sys.exit(EX_USAGE)

    # Parse opts for the image type to write
    imgtype = ".c"
    imgtarget = "std"
    memspace = "ram"
    outfn = None
    nativeFilename = None
    for opt in opts:
        if opt[0] == "-b":
            imgtype = ".bin"
        elif opt[0] == "-c":
            imgtype = ".c"
        elif opt[0] == "-s":
            imgtarget = "std"
        elif opt[0] == "-u":
            imgtarget = "usr"
        elif opt[0] == "--memspace":
            # Error if memspace switch given without arg
            if not opt[1] or (opt[1].lower() not in ["ram", "flash"]):
                print "Only one of these memspace types allowed: ram, flash"
                print __usage__
                sys.exit(EX_USAGE)
            memspace = opt[1]
        elif opt[0] == "--native-file":
            # Error if switch given without arg
            if not opt[1]:
                print "Specify a filename like this: --native-file=libnative.c"
                print __usage__
                sys.exit(EX_USAGE)
            nativeFilename = opt[1]
        elif opt[0] == "-o":
            # Error if out filename switch given without arg
            if not opt[1]:
                print __usage__
                sys.exit(EX_USAGE)
            outfn = opt[1]

    # Error if no image type was given
    if not imgtype:
        print __usage__
        sys.exit(EX_USAGE)

    # Error if no input filenames are given
    if len(args) == 0:
        print __usage__
        sys.exit(EX_USAGE)

    return outfn, imgtype, imgtarget, memspace, nativeFilename, args


def main():
    outfn, imgtyp, imgtarget, memspace, natfn, fns = parse_cmdline()
    pic = PmImgCreator()
    pic.set_options(outfn, imgtyp, imgtarget, memspace, natfn, fns)

    print "pmImgCreator: %s" % outfn

    pic.convert_files()
    pic.write_image_file()
    pic.write_native_file()


if __name__ == "__main__":
    main()
