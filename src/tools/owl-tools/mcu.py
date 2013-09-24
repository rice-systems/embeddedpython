# tools/user/mcu.py
#
# interface for programming and initializing microcontroller
#
# This file is Copyright 2007, 2009 Dean Hall.
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import cmd, getopt, os, subprocess, sys
from pmImgCreator import PmImgCreator, NoNativeFileException
import ipm
import locale
import connection
import toolchain

__usage__ = """USAGE:
    mcu -[s /dev/tty] --[serial=/dev/tty [baud=19200]
             [ image.bin | foo.py, bar.py, ... | [ ipm | desktop ] ]
    """

REPLY_TERMINATOR  = '\x04'
BAUD = 230400

locale.setlocale(locale.LC_ALL, '')

def U16_to_str(w):
    """Convert the 16-bit word, w, to a string of two bytes.

    The 2 byte string is in little endian order.
    DOES NOT INSERT TYPE BYTE.
    """

    return chr(w & 0xff) + \
           chr((w >> 8) & 0xff)

class Programmer(cmd.Cmd):
    def __init__(self, conn):
        cmd.Cmd.__init__(self,)
        self.conn = conn


    def send_command(self, cmd):
        self.conn.write(cmd)


    def program(self, fnames):
        if fnames[0].split('.')[-1] in ['py', 'owl', 'md']:
            print "compiling as %s:" % toolchain.describe_mode()
            codeimg = compile_image(fnames)
        else:
            print "flashing raw image: %s" % fnames[0]
            codeimg = open(fnames[0]).read()

        # include name and null terminator in code image
        # this is how pmImgCreator does things, so we should match
        fn = os.path.basename(fnames[0])
        mod_name = os.path.splitext(fn)[0]

        if not (0 < len(mod_name) < 254):
            print "ERROR: length of primary module (%s) must be between 1-255 characters" % mod_name
            sys.exit()
        
        # include offset of start of codeimg,
        # null-terminated module name and null-terminated code image
        codeimg = chr(len(mod_name)+2) + mod_name + '\x00' + codeimg + '\x00'

        # convert to hex and add header/footer
        expected_sum = reduce(lambda x,y: x ^ ord(y), codeimg, 0)
        print "using %s bytes of flash on target" % \
                    locale.format("%d", len(codeimg), grouping=True)
        codeimg = 'l' + ipm.tohex(codeimg) + 'xx'

        # print "CODEIMG: %s" % codeimg

        try:
            self.conn.write(codeimg)
            flash_response = self.conn.s.read(1)
            if not flash_response:
                print "ERROR: programming failed, response timed out"

            if flash_response == 'e':
                print "WARNING: programming succeeded after retries."
            elif flash_response == 'f':
                print "ERROR: programming failed after too many retries."
            elif flash_response == 's':
                print "flash succeeded."
            else:
                print "ERROR: programming failed (%s)" % flash_response

            reported_sum = int(self.conn.s.read(2), 16)
            if not reported_sum == expected_sum:
                print "ERROR: programming failed, incorrect checksum"
            else:
                print "programming verified!"
        except Exception, e:
            sys.stdout.write(
                "Serial write error.\n")


def compile_image(fnames):
    pic = PmImgCreator()
    pic.set_options('no_output_file', '.bin', 'usr', 'ram', None, fnames)
    pic.convert_files()
    
    codeobj = pic.formatFromExt[pic.imgtype]()
    return codeobj


def parse_cmdline():
    """Parses the command line for options.
    """
    baud = BAUD

    # see if we can see somebody on the wire
    try:
        serdev = connection.autodetect()
        Conn = ipm.SerialConnection
    except connection.AutodetectError, e:
        autodetect_error = "Autodetect error: %s" % e
        serdev = None

    # parse the arguments. if we see an invalid one, bail
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs",
            ["help", "serial=", "baud="])
    except Exception, e:
        print __usage__
        sys.exit()

    # if we didn't get enough arguments and couldn't autodetect, bail
    if (not opts) and (not serdev) and (not 'desktop' in args):
        print __usage__
        print autodetect_error
        sys.exit()

    if 'desktop' in args:
        Conn = connection.PipeConnection
        desktop = True
    else:
        Conn = connection.SerialConnection
        desktop = False

    for opt in opts:
        if opt[0] == "-s":
            serdev = args[0]
            if len(args) > 1:
                baud = int(args[1])
        elif opt[0] == "--serial":
            serdev = opt[1]
        elif opt[0] == "--baud":
            assert serdev, "--serial must be specified before --baud."
            baud = int(opt[1])
        else:
            print __usage__
            sys.exit(0)

    if Conn == connection.SerialConnection:
        c = Conn(serdev, baud)
    else:
        c = Conn()

    c.desktop = desktop

    return c, args

def do_args(conn, prog, args):
    if len(args) < 1 and not conn.desktop:
        print __usage__
        print "must specify action (ipm, program to flash, etc.)"
        sys.exit(0)
    if conn.desktop or args[0] == 'ipm':
        prog.send_command('i')
        i = ipm.Interactive(conn)
        i.run()
    elif args[0] == 'listen':
        conn.read()
    elif args[0] == 'run':
        prog.send_command('r')
        conn.read()
    elif args[0] == 'echo':
        prog.send_command('e')
    elif args[0] == 'fail':
        prog.send_command('x')
    else:
        prog.program(args)

def init_ipm(serdev):
    conn = connection.SerialConnection(serdev, BAUD)
    p = Programmer(conn)
    p.send_command('i')
    i = ipm.Interactive(conn)
    return i

def run(serdev, *args):
    conn = connection.SerialConnection(serdev, BAUD)
    p = Programmer(conn)
    do_args(conn, p, list(args))

def connect(serdev=None):
    if not serdev:
        serdev = connection.autodetect()

    conn = connection.SerialConnection(serdev, BAUD)
    p = Programmer(conn)
    do_args(conn, p, ['ipm'])    

def program(serdev, *args):
    programList(serdev, list(args))

def programList(serdev, argList):
    conn = connection.SerialConnection(serdev, BAUD)
    p = Programmer(conn)
    do_args(conn, p, argList)

def main():
    conn, args = parse_cmdline()
    p = Programmer(conn)

    try:
        do_args(conn, p, args)
    except NoNativeFileException:
        print "error: files containing native functions must be included at VM build time"

if __name__ == "__main__":
    main()
