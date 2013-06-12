# tools/user/toolchain.c
#
# This module is used to facilitate language research at Rice University. It
# can be used to switch the Owl environment between the Python toolchain and a
# custom one. In this version of the virtual machine, it does nothing.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import dis as python_dis
import sys

class Toolchain(object):
    PYTHON_TOOLS = {'dis': python_dis, 'compile': compile}
    MODES = ['python']
    
    def __init__(self):
        self.current_mode = self.MODES[0]

    def set_mode(self, mode):
        if mode in self.MODES:
            self.current_mode = mode
        else:
            raise NameError, "mode must be one of %s" % self.MODES

    def get_mode(self):
        return self.current_mode

    def describe_mode(self):
        return "CPython"

    def __getattr__(self, attr):
        return self.PYTHON_TOOLS[attr]

# replace the module with an instance of this class

# DANGER! Anything in the module scope here that's not referenced elsewhere
# will be garbage collected! Put it in the class!

sys.modules[__name__] = Toolchain()

