# tools/user/connection.py
#
# Serial and pipe connections to the VM.
#
# This file is Copyright 2007, 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

try:
    import serial
except ImportError:
    print "pyserial not detected."

from autodetect import AutodetectError, autodetect

import sys
import os
import os.path
import subprocess
import time

REPLY_TERMINATOR  = '\x04'
GROUP_SEPARATOR   = '\x1d'
RECORD_SEPARATOR  = '\x1e'
UNIT_SEPARATOR    = '\x1f'

# figure out where the relative platform/desktop/main.out is based
# on the location of this python file itself.
PMVM_EXE = os.path.abspath(os.path.dirname(__file__) + \
                           "/../../platform/desktop/main.out")

class ConnectionEndedException(Exception):
    pass

def save_profile(response):
    out = None
    in_block = False

    print "Profiler output seen in response. Enter filename to save."
    fn = raw_input("Filename (or enter to discard): ")

    if fn:
        fn = os.path.abspath(fn)

        for line in response.split('\n'):
            if line == '-start-':
                # only capture the last block
                in_block = True
                out = []
            elif line == '-end-':
                in_block = False
            else:
                if in_block:
                    out.append(line + '\n')

        if out:
            print "profiler output captured to %s" % fn
            f = open(fn, 'w+')
            f.writelines(out)
        else:
            print "profiler output empty. not saved."

class Connection(object):
    def open(self,): raise NotImplementedError
    def read(self,): raise NotImplementedError
    def write(self, msg): raise NotImplementedError
    def close(self,): raise NotImplementedError


class PipeConnection(Connection):
    """Provides ipm-host to target connection over stdio pipes on the desktop.
    This connection should work on any POSIX-compliant OS.
    The ipm-device must be spawned as a subprocess
    (the executable created when PyMite was built with PLATFORM=desktop).
    """
    def __init__(self, target=PMVM_EXE):
        self.open(target)
        self.desktop = True


    def open(self, target):
        self.child = subprocess.Popen(target,
                                      bufsize=-1,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      )

        print "Connecting to VM via pipe..."

        time.sleep(.1)
        self.failsafe()


    def read(self,echo=True, excfn=None):
        self.failsafe()
        response = ""
        in_exception = False
        excstart = None

        while True:
            character = self.child.stdout.read(1)
            if character == '':
                return response

            response += character

            if character == REPLY_TERMINATOR:

                if '-start-' in response:
                    save_profile(response)

                return response

            if character == GROUP_SEPARATOR:
                in_exception = (not in_exception)
                if in_exception:
                    excstart = len(response)
                elif excstart != None:
                    excfn(response[excstart:len(response)-1])
                continue

            if (not in_exception) and echo:
                sys.stdout.write(character)


    def failsafe(self):
        if self.child.poll():
            out = self.child.stdout.read()
            print "crashed! raw message: %s" % repr(out)

            exceptions = []
            current_exception = ""
            in_exception = False

            for c in out:
                if c == GROUP_SEPARATOR:
                    if in_exception:
                        exceptions.append(current_exception)
                    in_exception = (not in_exception)
                else:
                    current_exception += c

            if current_exception:
                exceptions.append(current_exception)
            
            for current_exception in exceptions:
                report_error(current_exception, verbose=True)

            sys.exit(1)


    def write(self, msg):
        self.child.stdin.write(msg)
        self.child.stdin.flush()


    def close(self,):
        self.write("\0")


class SerialConnection(Connection):
    """Provides ipm-host to target connection over a serial device.
    This connection should work on any platform that PySerial supports.
    The ipm-device must be running at the same baud rate (19200 default).
    """

    def __init__(self, serdev="/dev/cu.SLAB_USBtoUART", baud=19200):
        self.s = serial.Serial(serdev, baud)
        self.s.setRtsCts(1)
        self.s.setTimeout(4)
        self.desktop = False

        print "Connecting to VM via %s..." % serdev

    def read(self, echo=True, excfn=None):
        response = ""
        in_exception = False

        while True:
            try:
                character = self.s.read(1)
            except serial.serialutil.SerialException:
                raise ConnectionEndedException

            response += character

            if character == REPLY_TERMINATOR:

                if '-start-' in response:
                    save_profile(response)
                
                return response

            if character == GROUP_SEPARATOR:
                in_exception = (not in_exception)
                if in_exception:
                    excstart = len(response)
                elif excstart != None:
                    excfn(response[excstart:len(response)-1])
                continue

            if (not in_exception) and echo:
                sys.stdout.write(character)


    def write(self, msg):
        self.s.write(msg)
        self.s.flush()
            
    
    def close(self,):
        self.s.close()


