# lib/time.py
#
# CPython compatible timer module.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys

def time():
    return float(sys.time()) / 1000.0

def sleep(seconds):
    sys.sleep(int(1000*seconds))
