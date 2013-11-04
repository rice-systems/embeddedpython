#!/usr/bin/env python2.7
# tools/build/pmFeatures.py
#
# generates list of defines to pass to the compiler
#
# Copyright 2013 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

# search order:
# vm/default.defines
# platform/x/platform.defines
# platform/x/local.defines

import sys
import os.path
import os

DEFAULT_PATHS = [
    "../../vm/default.defines",
    "./platform.defines",
    "./local.defines"]

RULES = [('HAVE_CHRONOGRAPH', ['HAVE_BRIDGES', 'HAVE_MEDUSA'])]

class FeatureList(object):
    def print_defines(self):
        # say what we're doing to make debugging tractable
        sys.stderr.write("Active features:\n")
        sys.stderr.write("----------------\n")
        
        for define in self.defines:
            if self.values[define] is not None:
                sys.stderr.write("  %s=%s\n" % (define, self.values[define]))
            else:
                sys.stderr.write("  %s\n" % define)
        
        sys.stderr.write("----------------\n")

    def gen_gcc_invocation(self):
        args = []
        for define in self.defines:
            if self.values[define] is not None:
                args.append("-D%s=%s" % (define, self.values[define]))
            else:
                args.append("-D%s" % define)

        print " ".join(args)

    def load_file(self, fn):
        for line in open(fn):
            line = line.strip()

            # ignore comments and blank lines
            if not line:
                continue
            elif line[0] == '#':
                continue
            else:
                # we got a valid line, let's parse it
                # a plus or minus means something to add
                if line[0] == '+':
                    add_value = True
                elif line[0] == '-':
                    add_value = False
                else:
                    print "invalid syntax (line must start with +/-)", line
                    sys.exit(1)

                # chunk up the remaining into either a define or a define
                # and a value
                parts = line[1:].split()
                
                if len(parts) == 1:
                    key = parts[0]
                    value = None
                elif len(parts) == 2:
                    key = parts[0]
                    value = parts[1]
                else:
                    print "invalid syntax (line must contain key or key value)", line
                    sys.exit(1)

                # now actually record the value
                if add_value:
                    self.defines.add(key)
                    self.values[key] = value
                else:
                    self.defines.discard(key)
                    self.values[key] = None

    def verify(self):
        # make sure that prereqs are satisfied
        for feature, prereqs in RULES:
            if feature in self.features:
                for prereq in prereqs:
                    if prereq not in self.features:
                        sys.stderr.write("error! %s requires %s\n" % (feature, prereq))
                        sys.exit(1)
    
    def load_files(self):
        for path in DEFAULT_PATHS:
            base_path = sys.argv[1]
            define_path = os.path.join(base_path, path)

            # since local definitions are optional, only process files that are
            # there.
            if os.path.exists(define_path):
                self.load_file(define_path)

    def __init__(self):
        self.defines = set()
        self.values = {}

        self.load_files()
        self.print_defines()
        self.gen_gcc_invocation()

if __name__ == "__main__":
    f = FeatureList()

