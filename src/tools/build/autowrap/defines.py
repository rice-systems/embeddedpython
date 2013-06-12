# tools/build/autowrap/defines.py
#
# extracts macros from file
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.


import string, re

def process(preprocessed, filename, be):
    in_specified_file = False
    
    # this will be used to form a running evaluation of macro values
    values = {}

    for line in preprocessed.split('\n'):
        line = line.strip()

        # make sure this IS a preprocessor directive
        if not line.startswith('#'):
            continue

        # see if we're defining a new file location
        if line[2] in string.digits:
            if filename in line:
                in_specified_file = True
            else:
                in_specified_file = False

        # is this a macro?
        if line.startswith('#define'):
            define_match = re.search('define\s*(\S*)\s*(.*)', line)

            if define_match:
                # we do a running evaluation of everything using the uncleaned
                # namespace. this means that #defines that are defined in terms
                # of other #defines are properly converted into a single value.
                name, expr = define_match.groups()
                
                # the bare defines don't mean anything to us.
                if not expr:
                    continue

                # similarly, we really can't implement function macros
                if '(' in name:
                    continue

                try:
                    values[name] = eval(expr, values)
                except SyntaxError:
                    continue
                except NameError:
                    if in_specified_file:
                        be.comment("couldn't wrap macro: " + line)
                    continue

                if in_specified_file:
                    be.define(name, values[name])

