#!/usr/bin/env python
#
# tools/user/ide/connection_ed.py
#
# interface for programming and initializing microcontroller
# modified for ide
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import mcu, sys, ipm_ed, connection, connection_ed, serial, logging
import conditions

logger = logging.getLogger(__name__)


class Programmer(mcu.Programmer):
    def __init__(self, conn):
        mcu.Programmer.__init__(self, conn)

    def program_ed(self, stdout, fnames=[]):
        old_out = sys.stdout
        errstr = ''

        sys.stdout = stdout

        logger.debug('programming...')
        try:
            self.program(fnames)
        except Exception, e:
            if e:
                errstr = "%s:%s\n" % (e.__class__.__name__, e)
            logger.exception('program failed: %s', e)
            
        
        logger.debug('programming done')

        result = stdout.contents
        logger.debug('final: %s', result+'\n')
        
        sys.stdout = old_out

        return result, errstr


def do_args(conn, prog, args):
    if len(args) < 1 and not conn.desktop:
        print __usage__
        print "must specify action (ipm, program to flash, etc.)"
        sys.exit(0)
    if conn.desktop or args[0] == 'ipm':
        try:
            prog.send_command('i')
        except serial.SerialTimeoutException, se:
            args[1].put(se)
            args[3].serialerr = True
            return
        try:
            i = ipm_ed.Interactive(conn, queue=args[1],
            events=args[2], flags=args[3], cond=args[4])
        except Exception, e:
            logger.exception('ipm.__init__ failed')
            return
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
        return prog.program_ed(args[0], args[1:])


def connect(serdev=None, queue=None, events=None, flags=None, cond=None):
    if not serdev:
        serdev = connection.autodetect()
    try:
        conn = connection_ed.SerialConnection(serdev, mcu.BAUD,
                                       queue, events, cond, flags)
        flags.connected = True
        events.tryconnect.set()
    except serial.SerialException, se:
        conditions.get_from_q(queue)
        queue.put(se)
        flags.serialerr = True
        flags.connected = False
        events.tryconnect.set()
        return
    except Exception, e:
        conditions.get_from_q(queue)
        queue.put(e)
        flags.connected = False
        events.tryconnect.set()
        return
    p = Programmer(conn)
    do_args(conn, p, ['ipm', queue, events, flags, cond])

def program(serdev, *args):
    programList(serdev, argList=list(args))

def programList(serdev, argList=[], queue=None, events=None, flags=None):
    try:
        conn = connection_ed.SerialConnection(serdev, mcu.BAUD,
                    events=events, flags=flags)
        events.tryconnect.set()
    except serial.SerialException, se:
        logger.debug('se conn.init: %s', se)
        queue.put(str(se))
        flags.serialerr = True
        events.tryconnect.set()
        return
    
    p = Programmer(conn)
    try:
        logger.debug('do args:')
        result, errstr = do_args(conn, p, argList)
        if errstr:
            flags.err = True
        if result:
            queue.put(result)
            events.outputinq.set()
            if errstr:
                logger.debug('consoleready wait')
                events.consoleready.wait()
                events.consoleready.clear()
                queue.put(errstr)
            else:
                events.consoleready.clear()
            events.outputinq.set()
            logger.debug('outputinq')
    except serial.SerialException, se:
        queue.put(str(se))
        flags.serialerr = True        
        return

