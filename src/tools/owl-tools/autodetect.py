# tools/user/autodetect.py
#
# Autodetects serial ports on Linux and Mac.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.


import sys
import os

class AutodetectError(Exception):
    pass
    
def autodetect():
    if 'arwin' in sys.platform or 'linux' in sys.platform:
        devs = os.listdir('/dev/')

        if 'mcu' in devs:
            return '/dev/mcu'

        if 'arwin' in sys.platform:
            devs = [d for d in devs if 'tty.usb' in d]
        else:
            devs = [d for d in devs if 'ttyACM' in d]

        if len(devs) > 1:
            raise AutodetectError, "multiple USB serial devices found"
        if len(devs) < 1:
            raise AutodetectError, "no USB serial devices found"
        else:
            dev = '/dev/' + devs[0]
            return dev
    else:
        raise AutodetectError, "cannot autodetect on platform %s" % sys.platform

if __name__ == "__main__":
    print "autodetected: %s" % autodetect()
