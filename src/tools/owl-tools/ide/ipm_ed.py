# tools/user/ide/ipm_ed.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys, cmd
import toolchain
import ipm, logging, conditions, serial, objects

logger = logging.getLogger(__name__)

class Interactive(ipm.Interactive):
    def __init__(self, conn, queue, events, flags, cond):

        ipm.Interactive.__init__(self,conn)

        self.q = queue
        self.events = events
        self.cond = cond
        self.flags = flags
        self.ipmcommands += ('quit',)
        
        old_stderr = self.stderr
        old_syserr = sys.stderr

        err_writer = objects.qWriter(self.cond, self.q, self.events, self.flags, err=True)
        sys.stderr = err_writer
        self.stderr = err_writer

        out_writer = objects.qWriter(self.cond, self.q, self.events, self.flags)
        sys.stdout = out_writer
        self.stdout = out_writer

    def do_quit(self, *args):
        logger.debug('do_quit')
        logger.debug(self.q.qsize())
        self.conn.close()
        self.stop = True
        self.flags.disconnect = True
        self.events.connclose.set()
        return True

    def get_header(self):
        """
        gets the message at the start of the console
        """
        logger.debug('entering get_header')

        self.q.put(ipm.INIT_MESSAGE)

        self.q.put( "Using " + toolchain.describe_mode())
        

        try:
            info = self.eval_string('import build; build.show()')
            self.q.put('\n'+info)
            self.q.put(self.prompt)

        except serial.SerialException, se:
            conditions.get_from_q(self.q)
            self.q.put(se)
            self.flags.serialerr = True
        

        except ipm.PyMiteError:
            pass
            
        logger.debug('get_header done')


    def run(self):
        """
        command loop for interactive console
        """
        logger.debug('entering ipm.run')
        self.events.getheader.wait()
        self.get_header()
        self.events.haveheader.set()
        logger.debug('ipm.run: haveheader')
        
        self.stop = False
        while not self.stop:
            logger.debug('startloop waiting')
            self.events.startloop.wait()
            if self.flags.disconnect:
                self.do_quit()
                break
            continput = True
            try:
                continput, runcmd = conditions.get_item(self.cond,
                                    self.q, self.get_input)
            except Exception, e:
                logger.exception('get_item failed in run')
            self.events.inputdone.set()
            
            if runcmd:
                result = self.get_output()
                if not result:
                    self.flags.cmddone = True
                    self.events.outputinq.set()
                    if self.flags.disconnect:
                        logger.info('disconnect')
                        self.do_quit()
                        return
            #else: print result, do not run codeobj
            if self.flags.err: #print error message before
                                #printing prompt
                self.events.consoleready.clear()
                self.events.outputinq.set()
                self.events.consoleready.wait()
                self.events.consoleready.clear()
            if not continput:
                logger.debug('prompt')
                conditions.make_item(self.cond, self.q, item=self.prompt)
                self.flags.promptset = True
                self.flags.cmddone = True
                logger.debug('outputinq : 116')
                self.events.outputinq.set()
            self.events.startloop.clear()


    def get_output(self):
        """
        calls run_codeobj, prints any errors
        returns True if run_codeobj was completed sucessfully
        """
        logger.debug('entering get_output')
        if self.codeobj:
            try:
                self.run_codeobj(self.codeobj)
      
                if self.flags.disconnect:
                    logger.debug('get_output done -- disconnect')
                    return False
                return True
            except serial.SerialException, se:
                logger.debug('serial err: %s', se)
                self.q.put(se)
                self.flags.serialerr = True
                self.flags.disconnect = True
                logger.debug('get_output done -- serialerr')
                return False
            except AttributeError:
                #happens when response is None
                logger.debug('putting on q...')
                self.q.put('Connection read error: no response returned')
                logger.debug(self.q.qsize())
                self.flags.serialerr = True
                self.flags.disconnect = True
                logger.debug('get_output done -- attrerr')
                return False
            except Exception,e:
                logger.exception('get_output failed')
        logger.debug('leaving get_output -- other')
        return True
          



    def get_input(self,cmdnew):
        """
        gathers input from editor
        """
        logger.debug('entering get_input')
        try:
            if cmdnew is not None:
                line = cmdnew
            if not line:
                line = 'EOF'
            self.cmdnew = cmdnew
            continput, runcmd = self.checkcmd(line)
            logger.debug('leaving get_input: %s, %s', continput, runcmd)
            return continput, runcmd
        except Exception, e:
            logger.exception('get_input failed')
            return False, False

    def checkcmd(self, line):
        """
        checks for continued input and compiles line
        """
        self.codeobj = None
        # Ignore empty line, continue interactive prompt
        if (not line) or line.isspace():
            return False, False

        # Handle ctrl+D (End Of File) input, ignore unless quit?
        if line == "EOF":
            return False, False

        #check for line continuation character
        if line.endswith('\\'):
            self.flags.continput = True
            return True, False

        # check for multiline commands, get last line:
        lines = line.split('\n')
        newline = lines[-1].lstrip()

        #check for line cont char on prev line:
        if len(lines) > 1:
            if lines[-2].endswith('\\'):
                self.flags.continput = False

        # Handle ipm-specific commands
        command = line.split()[0]
        if command in self.ipmcommands:
            self.events.inputdone.set()
            cmd.Cmd.onecmd(self, line)
            return False, False
    
        if self.flags.parenerr:
            pass
        elif self.flags.continput:
            #gathers rest of indented block until blank line
            if not lines[-1].isspace():
                return True, False
            else:
                #finished gathering indented block
                line = '\n'.join(lines[:-1])
                logger.debug(' checkcmd final: %s',line)

        # Gather input from the interactive line
        codeobj = None

        # Try to compile the given line
        try:
            codeobj = toolchain.compile(line, ipm.COMPILE_FN, ipm.COMPILE_MODE)


        # Get more input if syntax error reports unexpected end of file
        except SyntaxError, se:
            if se.msg.startswith("unexpected EOF while parsing") or \
                    se.msg.startswith("expected an indented block"):
                if self.flags.parenerr: #mismatched brackets
                    logger.debug('paren err')
                    self.q.put("%s:%s\n" % (se.__class__.__name__, se))
                    self.flags.err = True
                    self.flags.contparen = False
                    return False, False
                if not (self.flags.contparen or self.flags.continput):
                    logger.debug('other eof')
                    self.q.put("%s:%s\n" % (se.__class__.__name__, se))
                    self.flags.err = True
                    return False, False
                else:
                    return True, False #open bracket

            else: #other syntax err
                if self.flags.contparen:
                    return True, False
        
                self.q.put("%s:%s\n" % (se.__class__.__name__, se))
                self.flags.err = True
                self.flags.continput = False
                return False, False

        self.flags.continput = False
        self.flags.contparen = False
        self.codeobj = codeobj
        return False, True

