# src/tools/user/profiler.py
#
# Parses python line number profiler.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys

def parse_profile(output):
    ticks = None
    freq = None

    ms_per_tick = 0.0

    lines = []

    for line in output.split('\n'):
        line = line.strip()

        if line.startswith('ticks: '):
            ticks = int(line.split('ticks: ')[1])
            
        if line.startswith('profiler frequency: '):
            freq = int(line.split('profiler frequency: ')[1])
            ms_per_tick = 1000.0/freq

        if line.startswith('l '):
            header, counts = line.split(': ')
            top, all_samples = [ms_per_tick * float(n) for n in counts.split('/')]
            lines.append((top, all_samples))
    
    print "total time: %.2f ms" % (ticks / float(freq) * 1000.0)
    return lines


def format_profile(raw_profile, source_fn=None):
    lines = parse_profile(raw_profile)

    if source_fn:
        print "profile of %s" % source_fn
        sources = [l.strip('\n') for l in open(source_fn)]
    else:
        sources = ["" for l in lines]

    for n in range(len(sources)):
        if not sources[n].strip():
            print "%3d:" % n
        else:
            try:
                print "%3d: %8.2f ms (%8.2f ms) : %s" % (n, lines[n][0], lines[n][1], sources[n])
            except IndexError:
                print "%3d:     -.-- ms (    -.-- ms) : %s" % (n, sources[n])


if __name__ == "__main__":
    format_profile(open(sys.argv[1]).read(), sys.argv[2])


