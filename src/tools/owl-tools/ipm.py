# tools/user/ipm.py
# ipm.py contains routines and objects for interactive prompt
#
# This file is Copyright 2007, 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import cmd, getopt, os, subprocess, sys, datetime, time
import pmImgCreator
import disassemble
from connection import *
import toolchain
from version import VERSION

DEFAULT_VERBOSE = True

# make sure we're running on a valid version of python
if not sys.version[:3] in ['2.7']:
    raise SystemError, "Must be running Python 2.7"

__fileids__ = {0x01:  'codeobj.c',
               0x02:  'dict.c',
               0x03:  'frame.c',
               0x04:  'func.c',
               0x05:  'global.c',
               0x06:  'heap.c',
               0x07:  'img.c',
               0x08:  'int.c',
               0x09:  'interp.c',
               0x0A:  'pmstdlib_nat.c',
               0x0B:  'list.c',
               0x0C:  'main.c',
               0x0D:  'mem.c',
               0x0E:  'module.c',
               0x0F:  'obj.c',
               0x10:  'seglist.c',
               0x11:  'sli.c',
               0x12:  'strobj.c',
               0x13:  'tuple.c',
               0x14:  'seq.c',
               0x15:  'pm.c',
               0x16:  'thread.c',
               0x17:  'float.c',
               0x18:  'class.c',
               0x19:  'xrange.c',
               0x1A:  'set.c',
               0x1D:  'packedtuple.c',
               0x1E:  'foreign.c'}

__errors__ = {0xFF: 'No result',
              0xFE: 'General failure',
              0xFD: 'Return value for stub function',
              0xFC: 'Assertion failure',
              0xFB: 'Modified frame pointer',
              0xE0: 'General exception',
              0xE1: 'System exit',
              0xE2: 'Input/output error',
              0xE3: 'Division by zero',
              0xE4: 'Assertion error',
              0xE5: 'Attribute error',
              0xE6: 'Import error',
              0xE7: 'Index error',
              0xE8: 'Key error',
              0xE9: 'Memory error',
              0xEA: 'Name error',
              0xEB: 'Syntax error',
              0xEC: 'System error',
              0xED: 'Type error',
              0xEE: 'Value error',
              0xEF: 'Stop iteration',
              0xF0: 'Warning',
              0xF1: 'rone error',
              0xF2: 'Unbound variable error'}

__eKeys__ = {0: 'Error      ',
             2: 'File       ',
             3: 'Line       ',
             4: 'Python File',
             5: 'Python Line',
             6: 'Info       ',
             8: 'Thread ID  ',
             7: 'Traceback (top first)'}

__eVals__ = {0: __errors__,
             2: __fileids__}

__eFormatters__ = {
    0xEA: ": name '%s' is not defined",
    0xE5: ": module does not have attribute '%s'",
    0xE8: ": key '%s' not found"}

COMPILE_FN = "<interactive>"
COMPILE_MODE = "single"
INIT_MESSAGE = """Owl Interactive Prompt (Toolchain v%s)
""" % VERSION

REPLY_TERMINATOR  = '\x04'
GROUP_SEPARATOR   = '\x1d'
RECORD_SEPARATOR  = '\x1e'
UNIT_SEPARATOR    = '\x1f'

def tohex(codeimg):
    out = []
    for byte in codeimg:
        unformatted = hex(ord(byte))
        formatted = unformatted.split('x')[1]
        formatted = '0'*(2-len(formatted)) + formatted

        out.append(formatted)

    return ''.join(out)


class PyMiteError(Exception):
    pass

class Interactive(cmd.Cmd):
    """The interactive command line parser accepts typed input line-by-line.
    If a statement requires multiple lines to complete,  the input
    is collected until two sequential end-of-line characters are received.
    """
    ipmcommands = ("?", "help", "run", "profile", "verbose", "dis")


    def __init__(self, conn):
        cmd.Cmd.__init__(self,)
        
        self.conn = conn
        conn.stdout = self.stdout
        self.stderr = sys.stderr
        self.last_err = None
        self.disassemble = False

        self.reset()

    def reset(self):
        self.pic = pmImgCreator.PmImgCreator()
        self.prompt = '%s> ' % toolchain.get_mode()

    def do_help(self, *args):
        """Prints the help message.
        """
        self.stdout.write(HELP_MESSAGE)
    
    def do_verbose(self, *args):
        if self.last_err:
            self.report_error(self.last_err, verbose=True)
        else:
            print "no saved error to report"

    def do_dis(self, *args):
        self.disassemble = not self.disassemble
        print "disassemble: %s" % self.disassemble

    def do_run(self, *args):
        self.run_file(args)

    def run_file(self, args, profile=None):
        """runs a module from the host to the target device.
        """

        # Ensure the filename arg names a python source file
        fn = args[0]
        if fn.endswith(".py"):
            toolchain.set_mode("python")
        else:
            self.stderr.write('Error using "run": \n'
                              'module must be a ".py" or ".md" source file.\n')
            return

        # reinit
        self.reset()
        
        try:
            file = open(fn)
        except IOError:
            self.stderr.write("Error using run: file %s not found\n" % fn)
            return

        try:
            codeobj = toolchain.compile(file.read(), fn, 'exec')
        except Exception, e:
            self.stderr.write("%s:%s\n" % (e.__class__.__name__, e))
            return
        
        self.run_codeobj(codeobj, profile=profile)


    def eval_string(self, cmdstr):
        """Executes cmdstr
        """
        # Try to compile the given line
        codeobj = None
        try:
            codeobj = toolchain.compile(cmdstr, COMPILE_FN, COMPILE_MODE)
        except SyntaxError, se:
            self.stderr.write("%s:%s\n" % (se.__class__.__name__, se))
            return

        # Run the compiled code object
        return self.run_codeobj(codeobj, fail_on_error=True, echo=False)


    def onecmd(self, line):
        """Gathers one interactive line of input (gets more lines as needed).
        """
        # Ignore empty line, continue interactive prompt
        if (not line) or line.isspace():
            return

        # Handle ctrl+D (End Of File) input, stop interactive prompt
        if line == "EOF":
            self.conn.close()

            # Do this so OS prompt is on a new line
            self.stdout.write("\n")

            # Quit the run loop
            self.stop = True
            return True

        # Handle ipm-specific commands
        if line.split()[0] in Interactive.ipmcommands:
            cmd.Cmd.onecmd(self, line)
            return

        # Gather input from the interactive line
        codeobj = None
        while not codeobj:

            # Try to compile the given line
            try:
                codeobj = toolchain.compile(line, COMPILE_FN, COMPILE_MODE)

            # Get more input if syntax error reports unexpected end of file
            except SyntaxError, se:
                if se.msg.startswith("unexpected EOF while parsing") or \
                        se.msg.startswith("expected an indented block"):
                    # Restore the newline chopped by cmd.py:140
                    line += "\n"

                    # Get more input if needed
                    while not line.endswith("\n\n"):
                        line += self.stdin.readline()
                else:
                    self.stderr.write("%s:%s\n" % (se.__class__.__name__, se))
                    return


            # Print any other exception
            #except Exception, e:
            #    self.stderr.write("%s:%s\n" % (e.__class__.__name__, e))
            #    return
            
        self.run_codeobj(codeobj)


    def run_codeobj(self, codeobj, fail_on_error=False, echo=True, profile=None):
        # DEBUG: Uncomment the next line to print the statement's bytecodes
        if self.disassemble:
            disassemble.show_module(codeobj)

        # Convert to a code image
        try:
            codeimg = self.pic.co_to_img(codeobj)
            
        # Print any conversion errors
        except Exception, e:
            self.stderr.write("%s:%s\n" % (e.__class__.__name__, e))

        # Otherwise send the image and print the reply
        else:

            # DEBUG: Uncomment the next line to print the size of the code image
            # print "DEBUG: len(codeimg) = ", len(codeimg)
            # DEBUG: Uncomment the next line to print the code image
            # print "DEBUG: codeimg = ", repr(codeimg)
            try:
                hexstr = 'c' + tohex(codeimg)
                self.conn.write(hexstr)
            except Exception, e:
                self.stderr.write(
                    "Serial write error.\n")

            rv = self.conn.read(echo=echo, excfn=self.report_error)

            if rv == '':
                self.stderr.write(
                    "Connection read error\n")
            else:
                # print "DEBUG: output from target: %s" % repr(rv)
                clean_output = rv.strip('\x04').strip('\n') + '\n'

                if not clean_output.strip():
                    clean_output = ''

                err_output = clean_output.split(GROUP_SEPARATOR)

                output = err_output[0]

                if len(err_output) > 1:
                    # Exception report
                    # try:
                    #     self.report_error(err_output[1])
                    # except KeyError:
                    #     print "error decoding new style exception, printing what's available"
                    #     pairs = err_output[1].split(RECORD_SEPARATOR)
                    #     for pair in pairs:
                    #         print pair.split(UNIT_SEPARATOR)

                    if fail_on_error:
                        raise PyMiteError

                if len(err_output) > 2:
                    output += err_output[2]

                # parse the profiler output if we got one
                if profile:
                    if 'python profiler' in output:
                        print "\nfound python profile report in output. parsed results:"
                        pyprofile.format_profile(output, profile)
                    else:
                        self.stdout.write("python profiler output not seen.\n")

                return output


    def run(self,):
        """Runs the command loop and handles keyboard interrupts (ctrl+C).
        The command loop is what calls self.onecmd().
        """

        print INIT_MESSAGE,

        print "Using", toolchain.describe_mode()

        try:
            info = self.eval_string('import build; build.show()')
            print info

        except PyMiteError:
            pass

        self.stop = False
        while not self.stop:
            try:
                self.cmdloop()
            except KeyboardInterrupt, ki:
                print "\n", ki.__class__.__name__
                # TODO: check connection?
            except ConnectionEndedException:
                print "Connection lost. Exiting."
                return

    def report_error(self, err, verbose=DEFAULT_VERBOSE):
        report_error(err, verbose, self)

def report_error(err, verbose=DEFAULT_VERBOSE, interactive=None):
    if interactive:
        interactive.last_err = err
    
    # decode everything from the exception
    pairs = err.split(RECORD_SEPARATOR)
    unpacked_pairs = [p.split(UNIT_SEPARATOR) for p in pairs]
    decoded_pairs = [(int(key, 16), val) for (key, val) in unpacked_pairs]

    exception_report = dict(decoded_pairs)

    error_code = int(exception_report[0], 16)
    name = __errors__[error_code]

    # this doesn't seem to always be valid. hunh.
    try:
        c_file = __fileids__[int(exception_report[2], 16)]
    except KeyError:
        c_file = "(unknown fileid %x)" % int(exception_report[2])

    c_line = exception_report[3]
    info = exception_report[6]
    traceback = exception_report[7].strip()
    try:
        tid = exception_report[8]
    except KeyError:
        tid = '(unknown)'

    # see how detailed we're going to be
    if verbose:
        print >> sys.stderr, "Exception in thread %s detected by %s:%s" % (tid, c_file, c_line)
        print >> sys.stderr, "Traceback (most recent call last):\n%s" % traceback
    else:
        print "Error detected:"
        traceback_lines = traceback.split('\n')
        print >> sys.stderr, traceback_lines[-1]
    
    # everybody gets the actual error code and info
    if error_code in __eFormatters__.keys():
        print >> sys.stderr, name + (__eFormatters__[error_code] % info)
    elif info:
        print >> sys.stderr, "%s: %s" % (name, info)
    else:
        print >> sys.stderr, name

