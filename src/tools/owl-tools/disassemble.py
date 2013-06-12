# tools/user/disassemble.py
#
# A general purpose python disassembler
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import toolchain
import sys
import types

def show_module(co):
    print "----------"
    print "name: %s" % co.co_name
    print "consts:"
    for n, const in enumerate(co.co_consts):
        print "  %d: %s" % (n, const)
    print "varnames: %s" % str(co.co_varnames)
    print "names: %s" % str(co.co_names)
    print "nlocals: %s" % co.co_nlocals
    print "argcount: %s" % co.co_argcount
    print "stack size: %s" % co.co_stacksize
    print "flags: %s" % hex(co.co_flags)
    print "disassembly: "
    toolchain.dis.dis(co)
    print "----------"
    for const in co.co_consts:
        if type(const) == types.CodeType:
            show_module(const)


if __name__ == "__main__":
    fname = sys.argv[1]
    code = open(fname).read()
    co = toolchain.compile(code, fname, 'exec')
    show_module(co)
