# tools/user/owl.py
#
# Simple front end to run a single file or spawn the interactive prompt
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import mcu, sys

def get_ipm():
    conn = mcu.connection.PipeConnection()
    conn.desktop = True
    return mcu.ipm.Interactive(conn)

def main():
    ipm = get_ipm()

    if len(sys.argv) == 1:
        ipm.run()
        sys.exit()
    elif len(sys.argv) == 2:
        ipm.do_run(sys.argv[1])
    else:
        print "owl: can only run one file at a time. import modules from the prompt"
        sys.exit(1)

if __name__ == "__main__":
    main()

