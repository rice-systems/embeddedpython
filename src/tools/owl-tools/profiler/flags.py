# src/tools/user/flags.py
#
# Analyzes time with flag set in profiles.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

FLAGS = ['sleep', 'gc', 'alloc', 'native', 'dict_getItem']

def parse_flag(profile, key, value):
    header, flag_num = key.split(' ')
    exclusive, total = value.split('/')

    profile.flags[FLAGS[int(flag_num)]] = (int(exclusive), int(total))

def analyze_flags(profile):
    sample_counts = {}
    profile.analyzed_flags = {}
    
    unaccounted_samples = profile.ticks

    # first, figure out what we DIDN'T account for
    for flag, (exclusive, total) in profile.flags.iteritems():
        unaccounted_samples -= exclusive
        sample_counts[flag] = exclusive
    sample_counts['other'] = unaccounted_samples

    # then transform them into times
    for flag in FLAGS:
        samples = sample_counts[flag]
        fraction = samples / float(profile.ticks)
        time = fraction * profile.time

        profile.analyzed_flags[flag] = (fraction, time)

    # now, let's look at the garbage collection data
    gc_time = profile.analyzed_flags['gc'][1]
    if profile.gc_invocations:
        profile.gc_avg_time = gc_time / profile.gc_invocations
    else:
        profile.gc_avg_time = None
        
    # now, let's look at the garbage collection data
    alloc_time = profile.analyzed_flags['alloc'][1]
    if profile.alloc_invocations:
        profile.alloc_avg_time = alloc_time / profile.alloc_invocations
    else:
        profile.alloc_avg_time = None


def print_flags_analysis(profile):
    print "gc invocations: %d" % profile.gc_invocations
    print "(collected %d samples in GC)" % profile.flags['gc'][0]
    if profile.gc_avg_time:
        print "avg gc time: %f ms\n" % (profile.gc_avg_time*1000.0)
    
    print "alloc invocations: %d" % profile.alloc_invocations
    print "(collected %d samples in alloc)" % profile.flags['alloc'][0]
    if profile.alloc_avg_time:
        print "avg alloc time: %f us\n" % (profile.alloc_avg_time*1000000.0)
    
    for (flag, (fraction, time)) in profile.analyzed_flags.iteritems():
        print "%s: %.1f%%, %f ms" % (flag, 100*fraction, 1000*time)
