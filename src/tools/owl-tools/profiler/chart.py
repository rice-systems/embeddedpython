# src/tools/user/chart.py
#
# Generate a pretty LaTeX chart of profiler results.
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import profile as profile_module
import sys
import dis

FRACTION = 1
AVG_EX_TIME = 2

MODE = FRACTION

opmap = dis.opmap
opmap["<255>"] = 255

opname = dis.opname[:]
opname[255] = "(garbage collector)"

# sorted into some kind of order.
opgroups = [25, 96, 126, 98, 91, 50, 51, 52, 53, 61, 18, 105, 135, 100, 136, 124, 116, 82,
101, 95, 137, 125, 97, 54, 90, 40, 41, 42, 43, 60, 23, 64, 21, 26, 62, 22, 20,
66, 19, 63, 24, 27, 65, 55, 77, 58, 28, 75, 59, 57, 79, 67, 76, 56, 29, 78, 13,
15, 11, 12, 10, 80, 89, 103, 104, 133, 102, 131, 141, 140, 142, 106, 119, 4,
99, 88, 85, 143, 93, 68, 108, 107, 84, 113, 110, 111, 112, 134, 132, 9, 87, 1,
70, 71, 73, 72, 74, 130, 83, 5, 3, 2, 121, 122, 120, 30, 31, 32, 33, 92, 81,
86, 255]

def format_output(collected_results):
    print "% profiler collected results"
    print "Bytecode/Benchmark & " + " & ".join(["\\begin{sideways} " + x[0] + "\\end{sideways}" for x in collected_results]) + " \\\\"

    print "\midrule"

    for bc in opgroups:
        bc_name = opname[bc]
        bc_name = bc_name.replace('_', '\_')

        # format the results
        if MODE == FRACTION:
            num_results = ["%d\%%" % (100.0*(x[1][bc])) for x in collected_results]
            num_results = [s if s != "0\%" else "-" for s in num_results]
        elif MODE == AVG_EX_TIME:
            num_results = []
            for x in collected_results:
                time = x[1][bc]
                if time:
                    num_results.append("%.1f" % (time*1000000))
                else:
                    num_results.append("-")

        # see if they're ALL zeros:
        all_zeros = True

        for res in num_results:
            if not res == '-':
                all_zeros = False

        if all_zeros:
            continue

        # print them into a row
        print "%s & " % bc_name \
          + " & ".join(num_results) + \
          " \\\\"

if __name__ == "__main__":
    collected_results = []

    for fn in sys.argv[1:]:
        fn_short = fn.split('/')[-1].split('.')[0].replace('_', '\_')
        single_result = [0.0] * 256
        
        profile = profile_module.Profile()
        profile.read_from_file(fn)

        profile.analyze()

        items = list(profile.analyzed_bcodes.iteritems())
    
        for (bcode, (fraction, total_time, execution_time)) in items:
            if MODE == FRACTION:
                single_result[dis.opmap[bcode]] = fraction
            elif MODE == AVG_EX_TIME:
                if fraction < 0.01:
                    single_result[dis.opmap[bcode]] = None
                else:
                    single_result[dis.opmap[bcode]] = execution_time
            else:
                print "invalid mode"
                sys.exit(1)

        collected_results.append((fn_short, single_result))

    format_output(collected_results)
