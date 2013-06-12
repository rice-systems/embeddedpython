# tools/build/autowrap/test_backend.py
#
# test backend for development
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

from clean import Cleaner

class TestBackend(object):
    def __init__(self, fn):
        self.fn = fn
        self.cleaner = Cleaner(fn)

    def comment(self, text):
        print "\n#", text

    def define(self, name, val):
        name = self.cleaner.clean(name)
        print "%s = %s" % (name, val)

    def function(self, ret_type, name, args):
        name = self.cleaner.clean(name)
        
        print "%s %s" % (ret_type, name)

        for t, n in args:
            print " %s %s" % (t, n)
