# tools/user/ide/connection_ed.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

# connection related classes and functions
# modified for ide

import conditions, threading, connection, serial, logging
logger = logging.getLogger(__name__)

class SerialConnection(connection.SerialConnection):
    def __init__(self, serdev, baud, queue=None, events=None, cond=None, flags=None):

        connection.SerialConnection.__init__(self, serdev,
                                             baud)
        self.q = queue
        self.cond = cond
        self.events = events
        self.flags = flags


    def read(self, echo=True, excfn=None):
        logger.debug('entering conn.read')
        response = ""
        in_exception = False
        had_exception = False
        
        if self.events:
            self.events.consoleready.set()

        while True:
            character = self.s.read(1)
            response += character
            
            if self.events: 
                if self.events.startloop.is_set():
                    self.events.consoleready.wait()
                    self.events.consoleready.clear()

   
                if self.flags.disconnect or self.flags.serialerr:
                    logger.debug('leaving conn.read -- disconnecting')
                    return
                
            if character == connection.REPLY_TERMINATOR:
                if '-start-' in response:
                    connection.save_profile(response)
                if self.q and self.events.startloop.is_set() and \
                       (not had_exception) and len(response)>1:
                    logging.debug('output not done')
                    conditions.make_item(self.cond, self.q, item=response[:-1]+'\n')
                    self.events.outputinq.set()
                    self.events.consoleready.wait()
                logger.debug('leaving conn.read -- reply done')
                return response

            if character == connection.GROUP_SEPARATOR:
                in_exception = (not in_exception)
                had_exception = True
                if in_exception:
                    excstart = len(response)
                    self.events.consoleready.set()
                elif excstart != None:
                    excfn(response[excstart:len(response)-1])
                continue

            if (not in_exception) and echo:
                if not self.q:
                    sys.stdout.write(character)
                else:
                    try:
                        if character == '\n':
                            conditions.make_item(self.cond, self.q,
                                                item=response )
                            response = ''
                            self.events.outputinq.set()
                        else:
                            self.events.consoleready.set()
                    except Exception, e:
                        logger.exception('read failed')
            else:
                self.events.consoleready.set()
