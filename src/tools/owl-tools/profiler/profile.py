# src/tools/user/profile.py
#
# Parses Owl profiler output.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.


import sys
import bcodes
import flags

# make sure we're running on a valid version of python
if not sys.version[:3] in ['2.7']:
    raise SystemError, "Must be running Python 2.7"

class Profile(object):
    def __init__(self):
        self.fn = '(none)'
        self.rate = 0
        self.ticks = 0
        self.bcodes = {}
        self.total_bcodes = 0
        self.flags = {}

    parse_bc = bcodes.parse_bc
    analyze_bcodes = bcodes.analyze_bcodes
    print_bcode_analysis = bcodes.print_bcode_analysis

    parse_flag = flags.parse_flag
    analyze_flags = flags.analyze_flags
    print_flags_analysis = flags.print_flags_analysis

    def read_from_file(self, fn):
        self.fn = fn

        for line in open(fn):
            line = line.strip()

            if not line:
                continue

            if line == "profiler stats:":
                continue

            try:
                key, value = line.split(": ")
            except ValueError:
                print "error parsing line: %s" % line
                sys.exit(1)

            if key == "profiler frequency":
                self.frequency = float(value)
                self.period = 1/float(value)

            if key == "ticks":
                self.ticks = int(value)

            if key == "bytecodes":
                self.total_bcodes = int(value)

            if key.startswith('bc'):
                self.parse_bc(key, value)

            if key.startswith('flag'):
                self.parse_flag(key, value)

            if key == 'gc':
                self.gc_invocations = int(value)

            if key == 'alloc':
                self.alloc_invocations = int(value)

            if key == "gc_in_sleep":
                self.gc_ticks_in_sleep = int(value)

    def analyze(self):
        self.time = self.period * self.ticks
        self.analyze_bcodes()
        self.analyze_flags()

    def print_stats(self):
        print "profile name: %s" % self.fn
        print "profiler frequency: %f" % self.frequency
        print "total time: %f sec" % self.time
        print "samples: %d" % self.ticks
        print "bytecodes executed: %d" % self.total_bcodes
        print "average bytecode execution time: %f us" % \
            (1000000.0* self.time / self.total_bcodes)

if __name__ == "__main__":
    fn = sys.argv[1]
    profile = Profile()
    profile.read_from_file(fn)

    profile.analyze()
    
    profile.print_stats()
    print ""
    profile.print_flags_analysis()
    print ""
    profile.print_bcode_analysis()

