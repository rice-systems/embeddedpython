# tools/user/ide/files.py
#
# locate magic files regardless of location, even in a py2exe
#
# Copyright 2013 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import os.path
import sys

GLADE_FILE = "projecttree.glade"
ICON_FILE = "owl.png"

def glade():
    return find_file(GLADE_FILE)

def icon():
    return find_file(ICON_FILE)

def find_file(fn):
    # first, check to see if we're running from py2exe
    if hasattr(sys, "frozen"):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(__file__)

    # now, combine that with the file name we want
    path = os.path.join(directory, fn)
    return path
