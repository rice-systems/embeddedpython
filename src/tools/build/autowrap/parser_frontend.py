# tools/build/autowrap/parser_frontend.py
#
# uses PyCParser to read the header files. complete rewrite from the old stuff.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys
from autowrap_backend import AutowrapBackend as Backend
import defines

sys.path.insert(0, '/home/tbarr/pycparser')

from pycparser import c_parser, c_ast, parse_file, preprocess_file

DEFINES = ['STM32F4']
ENUM_TYPE = 'int'

class UnsupportedType(Exception):
    pass

class Visitor(c_ast.NodeVisitor):
    def __init__(self, backend):
        self.backend = backend

    def visit_Enum(self, node):
        # for informational purposes, print the name as a comment
        name = node.name
        self.backend.comment("enumerator: " + name)
        
        # the C99 spec says that enumerators without defined numbers are
        # incremented from the previous number
        current_num = 0
        for enumerator in node.values.enumerators:
            if enumerator.value:
                val = int(enumerator.value.value)
                self.backend.define(enumerator.name, val)
                current_num = val + 1
            else:
                self.backend.define(enumerator.name, current_num)
                current_num += 1


    def visit_FuncDecl(self, node):
        # get the name of the function and its return type
        decl = node.type
        name = decl.declname
        return_type = ' '.join(decl.type.names)

        args = []

        # unpack the arguments
        for (_, arg) in node.args.children():
            if isinstance(arg.type.type, c_ast.IdentifierType):
                # standard return type
                arg_type = ' '.join(arg.type.type.names)
                
                # don't bother with void types
                if arg_type == 'void':
                    continue

            elif isinstance(arg.type.type, c_ast.Enum):
                # enums are actually integers
                arg_type = ENUM_TYPE
            else:
                raise UnsupportedType, "return type neither basic type nor enum"

            args.append((arg_type, arg.name))

        self.backend.function(return_type, name, args)

def clean_directives(preprocessed):
    out = []

    for line in preprocessed.split('\n'):
        if line.strip().startswith('#'):
            continue
        else:
            out.append(line)

    return "\n".join(out)

def frontend():
    # first thing we do is to run everything through the C preprocessor
    filename  = sys.argv[1]
    incdirs = sys.argv[2:]
    
    inc_args = [r'-I%s' % d for d in incdirs]
    def_args = [r'-D%s' % d for d in DEFINES]
    cpp_args = [r'-dD', '-undef']
    
    preprocessed = preprocess_file(filename, cpp_args=(inc_args + def_args + cpp_args))

    # now, fire up the backend and process the #defines
    be = Backend(filename)
    defines.process(preprocessed, filename, be)

    # strip out the directives so that we can actually parse the code
    preprocessed = clean_directives(preprocessed)

    # finally, go through the C file and get the enums and function defintions
    p = c_parser.CParser()
    ast = p.parse(preprocessed, filename)

    v = Visitor(be)
    v.visit(ast)
    
if __name__ == "__main__":
    frontend()

