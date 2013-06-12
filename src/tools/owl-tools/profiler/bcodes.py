# src/tools/user/profiler.py
#
# Analyzes bytecode use in profiles.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import dis
import sys
sys.path.insert(0, '/home/tbarr/owl/src/tools/medusa')
from opcode import opname

opname[255] = '(gc)'

if 'latex' in sys.argv:
    OUTPUT_FORMAT = "%s & %2.1f\\%% & %0.1f us & %d calls & %.1f us \\\\"
else:
    OUTPUT_FORMAT = "%s: %2.1f%%, %0.0f us / %d calls = %f us"


def parse_bc(profile, key, value):
    header, bcode = key.split(' ')
    samples, count = value.split('/')

    profile.bcodes[opname[int(bcode)]] = (int(samples), int(count))

def analyze_bcodes(profile):
    profile.analyzed_bcodes = {}

    for (bcode, (samples, count)) in profile.bcodes.iteritems():
        fraction_of_time = float(samples) / float(profile.ticks)
        time_in_bcode = fraction_of_time * profile.time
        time_per_execution = time_in_bcode / float(count)

        profile.analyzed_bcodes[bcode] = (fraction_of_time, time_in_bcode, time_per_execution)

def print_bcode_analysis(profile):
    items = list(profile.analyzed_bcodes.iteritems())
    items.sort(key=lambda x: x[1][0], reverse=True)
    for (bcode, (f, tt, et)) in items:
        if profile.bcodes[bcode][0]:
            print OUTPUT_FORMAT % \
                (bcode, f*100, 1000000*tt, profile.bcodes[bcode][1], 1000000*et) 

