# src/tools/user/profiler.py
#
# Parses output of mostly defunct memory profiler.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys, operator

types = {0x00:'NON',
         0x01:'INT',
         0x02:'FLT',
         0x03:'STR',
         0x04:'TUP',
         0x05:'COB',
         0x06:'MOD',
         0x07:'CLO',
         0x08:'FXN',
         0x09:'CLI',
         0x0A:'CIM',
         0x0B:'NIM',
         0x0C:'NOB',
         0x0D:'THR',
         0x0F:'BOL',
         0x10:'CIO',
         0x11:'MTH',
         0x12:'LST',
         0x13:'DIC',
         0x19:'FRM',
         0x1A:'BLK',
         0x1B:'SEG',
         0x1C:'SGL',
         0x1D:'SQI',
         0x1E:'NFM'}

def read_profile(fname):
    objects = []
    for line in open(fname):
        line = line.strip()

        if not line:
            continue

        type_code, remainder = line.split(": ")
        total_bytes, count = remainder.split("/")

        if count == '0':
            continue

        objects.append((types[int(type_code)], int(total_bytes), int(count)))

    return objects

if __name__ == "__main__":
    parsed_profile = read_profile(sys.argv[1])
    
    total_bytes = sum([t[1] for t in parsed_profile])
    total_objs = sum([t[2] for t in parsed_profile])

    parsed_profile.sort(key=operator.itemgetter(2), reverse=True)

    print "total bytes: %d" % total_bytes
    print "total objs: %d" % total_objs

    for (type_name, size, count) in parsed_profile:
        fraction = 100.0 * size / total_bytes
        average = float(size) / count

        print "%s: %d objs, %d bytes (%f b/obj, %1.2f%%)" % (type_name, count, size, average, fraction)
