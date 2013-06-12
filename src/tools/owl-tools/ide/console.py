# tools/user/ide/console.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import threading, Queue, re, time, logging, os, sys
import gtk, gobject, pango
import widgets, conditions, objects, dialogs

logger = logging.getLogger(__name__)


class Console(widgets.TextView):

    __gsignals__ = {'quit-signal' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                     (gobject.TYPE_BOOLEAN,)),
                    'conn-fail' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                    (gobject.TYPE_STRING,)),
                    'reset-alert': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                    ()),
                    'crash': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                    ()),
                    'in-cmd' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                     (gobject.TYPE_BOOLEAN,))}

                    
    def __init__(self, queue, events, flags, cond, edtree):
        widgets.TextView.__init__(self, 'console')

        self.connect('key-press-event',self.on_key_press)

        self.set_name('console')

        self.events = events
        self.q = queue
        self.cond = cond
        self.flags = flags
        self.edtree = edtree
        self.cmdlist = ['']
        self.cmdindex = 0
        self.offset = 0 #indent for open paren
        self.keep_cursor_pos = False
        self.in_cmd = 0

        self.writer = objects.Writable(self)

        self.err_txt = self.get_buffer().create_tag('err_text', foreground='red')
        self.header_txt = self.get_buffer().create_tag('header_txt', foreground='white')
        self.program_txt = self.get_buffer().create_tag('program_txt', foreground='black')
        output_color = gtk.gdk.Color(.76,.81,.85)
        self.output_txt = self.get_buffer().create_tag('output_txt',foreground_gdk=output_color,
                                                       weight=pango.WEIGHT_NORMAL) 
        self.get_buffer().found_txt = self.get_buffer().create_tag('found', background = gtk.gdk.Color('#CCCCFF'))

        #self.connect()
    
    def initialize(self):
        logger.debug('entering console.initialize')
        self.set_editable(True)
        logger.debug('getheader : 54')
        self.newprompt = False
        self.events.getheader.set()
        if not self.events.haveheader.wait(3):
            if self.flags.serialerr:
                logger.debug('option 1!')
                msg = self.q.get()
                logger.debug('serial err msg: %s', msg)
                self.emit('conn-fail', msg)
            else:
                logger.debug('option 2!')
                try:
                    self.flags.serialerr = True
                    self.emit('conn-fail','Connection failed: could not read from connection' \
                                        '\n\nPlease reset board and restart application')
                except:
                    logger.exception('conn-fail')
            return False
            
        logger.debug('haveheader')
         #starts ipm, gets initmsg
        tvbuffer = self.get_buffer()
        tvbuffer.begin_not_undoable_action()
            
        result = conditions.get_from_q(self.q)
        self.prompt = result.split('\n')[-1]
        self.writer.set_tag(self.header_txt)
        print >>self.writer, '\n'+result,
        enditer = tvbuffer.get_end_iter()
        tvbuffer.create_mark('cmd_start',enditer,True)
        
        
        logger.debug('leaving console.initialize')
        return True


    def on_close(self, widget):
        self.flags.disconnect = True

    def run_cmd(self, inputline=None):
        logger.debug('entering run_cmd')
        self.cmdindex = 0
        text = self.get_input(inputline)
        logger.debug('startloop set 98')
        self.events.startloop.set()
            #input on q, ipm goes
        logger.debug('inputdone waiting....')
        self.events.inputdone.wait()
        logger.debug('inputdone!')
        
        if not self.flags.continput and \
                 not self.flags.contparen:
            moreoutput = True
            self.put_onscreen('\n')
            while moreoutput:
                moreoutput = self.get_output()
                logger.debug('moreoutput: %s', moreoutput)
                if self.flags.serialerr:
                    msg = conditions.get_from_q(self.q)
                    logger.debug('serialerr msg: %s',msg)
                    self.emit('conn-fail', msg)
                    self.emit('quit-signal', False)
                    return
                if self.flags.disconnect:
                    logger.info('consolekill')
                    self.emit('quit-signal',False)
                    logger.debug('leaving run_cmd')
                    return

            tvbuffer = self.get_buffer()
            enditer = tvbuffer.get_end_iter()
            promptstart = tvbuffer.create_mark('cmd_start',enditer,True)
        else:
            self.print_result(text)

        logger.debug( 'ipm done')
           
        if self.flags.disconnect:
            logger.debug('disconnecting in console')
            self.emit('quit-signal',False)
        
        if not self.in_cmd:
            if self.cmdlist[0]:
                self.cmdlist = self.cmdlist[1:]
            self.in_cmd = True
        
        logger.debug('leaving run_cmd')

    def kill(self, widget=None):
        
        #should produce alert box, disconnect
        self.flags.disconnect = True
        self.emit('quit-signal',False)
        self.emit('reset-alert')
        return True


    def on_key_press(self, widget=None, event=None, inputline=None):
        if not self.get_editable() or self.flags.disconnect:
            return True
        if not event or event.keyval == 65293:
        #enter
            self.flags.cmddone = False
            self.emit('in-cmd', False)
            connect_b = self.edtree.get_widget('console_toggle_connect')
            if os.name != 'nt':
                connect_b.set_sensitive(False)
                handler = None
            else:
                handler = connect_b.connect('clicked', self.kill)
            self.set_editable(False)
    
            self.run_cmd(inputline)
            
            self.emit('in-cmd', True)
            if os.name == 'nt':
                connect_b.disconnect(handler)
            else:
                connect_b.set_sensitive(True)
            self.set_editable(True)
            self.events.inputdone.clear()
            return True
                
        elif event.keyval == 65362 or event.keyval == 65364:
            #up and down arrows, scroll through input history
            tvbuffer = self.get_buffer()
            hereiter = tvbuffer.get_iter_at_mark(tvbuffer.get_insert())
            if hereiter.can_insert(True):
                self.keep_cursor_pos = True
                if self.in_cmd:
                    self.in_cmd = False
                    end_mark = tvbuffer.create_mark('cmd_end',
                    tvbuffer.get_end_iter(),True)
                    text = self.get_cmd()
                    if text:
                        if len(text.split('\n')) > 1:
                            text = text.split('\n')[-1]
                        self.cmdlist = [text] + self.cmdlist
                if event.keyval == 65362:
                    self.cmdindex -= 1
                    if abs(self.cmdindex) > len(self.cmdlist):
                        self.cmdindex = -1
                elif event.keyval == 65364:
                    self.cmdindex += 1
                    if self.cmdindex > len(self.cmdlist)-1:
                        self.cmdindex = 0                
                text = self.cmdlist[self.cmdindex]
                enditer = tvbuffer.get_end_iter()
                startiter = tvbuffer.get_iter_at_line(enditer.get_line())
                if tvbuffer.get_text(startiter, enditer).startswith(self.prompt):
                    startiter = tvbuffer.get_iter_at_line_offset(enditer.get_line(),
                                                                 len(self.prompt))
                tvbuffer.delete(startiter, enditer)
                
                enditer = tvbuffer.get_end_iter()
                tvbuffer.insert(enditer, text)
                self.keep_cursor_pos = False
                return True

        elif event.keyval == 65361:
            #left arrow, should stop scrolling through
            #text at beginning of current prompt
            tvbuffer = self.get_buffer()
            hereiter = tvbuffer.get_iter_at_mark(tvbuffer.get_insert())
            try:
                startiter = tvbuffer.get_iter_at_mark(tvbuffer.get_mark('cmd_start'))
            except:
                return
            if startiter.get_offset() == hereiter.get_offset():
                return True
        else:
            if not self.in_cmd:
                if self.cmdlist[0]:
                    self.cmdlist = self.cmdlist[1:]
                self.in_cmd = True
        
            tvbuffer = self.get_buffer()
            try:
                enditer = tvbuffer.get_mark('cmd_start')
                insert = tvbuffer.get_iter_at_mark(tvbuffer.get_insert())
                if insert.in_range(tvbuffer.get_start_iter(), enditer):
                    tvbuffer.place_cursor(tvbuffer.get_end_iter())
            except:
                tvbuffer.place_cursor(tvbuffer.get_end_iter())

    def get_input(self, inputline):
        try:
            tvbuffer = self.get_buffer()
            end_mark = tvbuffer.create_mark('cmd_end', 
                tvbuffer.get_end_iter(),True)
                
            if not inputline:
                text = self.get_cmd()
                self.check_cmd(text)
            else:
                tvbuffer = self.get_buffer()
                text = inputline
                self.newprompt = True
                enditer = tvbuffer.get_end_iter()
                tvbuffer.insert(enditer, text)

            cmdnew = text.split('\n')[-1]
            if cmdnew and not cmdnew.isspace() and \
                self.cmdlist[-1] != cmdnew:
                logger.debug('cmdnew: %s',cmdnew)
                self.cmdlist.append(cmdnew)
            
            logger.debug('cmd: %s',text)
            conditions.make_item(self.cond, self.q, item=text)
            return text
        except Exception, e:
            logger.exception('console.get_input failed')
    
    def get_output(self):
        while not self.events.outputinq.is_set():
            logger.debug('waiting.5..')
            self.events.outputinq.wait(.5)
            if self.flags.disconnect:
                logger.debug('leaving get_output -- disconnect from while')
                return False
            logger.debug('mainiter...')
            while gtk.events_pending():
                gtk.mainiteration(gtk.FALSE)
        logger.debug('outputinq')
        self.events.outputinq.clear()
        if self.flags.disconnect:
            logger.debug('leaving get_ouput -- disconnect outside while')
            return False
        if self.flags.serialerr:
            logging.debug('leaving get_output -- serialerr')
            return False
        conditions.get_item(self.cond, self.q, self.parse_result)
        logger.debug('consoleready set : 280')
        self.events.consoleready.set()
        if not self.flags.cmddone:
            logger.debug('leaving get_output -- not cmddone')
            return True
        logger.debug('leaving get_output -- cmddone')
        if self.flags.promptset:
            conditions.get_item(self.cond, self.q, self.parse_result)
        return


    def parse_result(self,result):
        if result == '\n\n':
            return
        if result:
            if self.flags.err:
                self.print_error(result)
            else:
                self.print_result(result)
        while gtk.events_pending():
            gtk.mainiteration(gtk.FALSE)

        

    def print_result(self,result):
        if self.flags.continput or self.flags.contparen:
            result = self.autoindent(result)
        if self.newprompt:
            if self.flags.cmddone and '>' in result:
                logger.debug('prompt: %s',self.prompt)
                self.prompt = result
                self.newprompt = False
        if self.prompt in result:
            self.writer.set_tag(self.header_txt)
            self.flags.promptset = False
        else:
            self.writer.set_tag(self.output_txt)
        self.writer.write(result)
        if not self.flags.continput and \
         not self.flags.contparen:
            tvbuffer = self.get_buffer() 
            startiter, enditer = tvbuffer.get_bounds()
            tvbuffer.apply_tag(self.not_editable, startiter, enditer)

    def autoindent(self, result):
        logger.debug('autoindent: moreinput')
        lines = result.split('\n')
        lastline = lines[-1]
        indent_count = 0
        result = '\n'#+lines[-1]
        while lastline.startswith('\t'):
            indent_count += 1
            lastline = lastline[1:]
        result += '\t'*(indent_count)
        if self.flags.contparen:
            for i in xrange(self.offset):
                result += ' '
        elif lastline.endswith(':') or lastline.endswith('\\'):
            logger.debug('indent more')
            result += '\t'
        return result



    def print_error(self, result):
        try:
            if result.startswith('Connection write error') and \
               not self.flags.serialerr:
                self.connect_alert(result)
                self.toggle_connect(value=False)
            logger.debug( 'print err')
            self.writer.set_tag(self.err_txt)
            self.writer.write(result)
            self.flags.err = False
        except Exception, e:
            logger.exception('print error failed')

    def put_onscreen(self, text):
        tvbuffer = self.get_buffer()
        start, end = tvbuffer.get_bounds()
        tvbuffer.insert(end, text)
        enditer = tvbuffer.get_end_iter()
        tvbuffer.place_cursor(enditer)
        self.scroll_mark_onscreen(tvbuffer.get_insert())

        

    def get_cmd(self):
        logger.debug('cmdlist: %s', self.cmdlist)

        tvbuffer = self.get_buffer()
        cmd_start = tvbuffer.get_mark('cmd_start')
        startiter = tvbuffer.get_iter_at_mark(cmd_start)
        cmd_end = tvbuffer.get_mark('cmd_end')
        enditer = tvbuffer.get_iter_at_mark(cmd_end)
        text = tvbuffer.get_text(startiter, enditer)
            
        logger.debug( 'check: '+ text)

        return text

    def check_cmd(self, text):
        """
        now checks entire command entered, not just most recent line
        """
        #checks for open brackets:1
        if text.startswith('lang'):
            logger.debug('New prompt!')
            self.newprompt = True
        if text.endswith(':'):
            self.flags.continput = True
        brackets = [('(',')'),('[',']'),('{','}')]
        count_data = [0,0,0]
        self.offset = 0 #open paren indent
        for i in xrange(3):
            open_count = text.count(brackets[i][0])
            close_count = text.count(brackets[i][1])
            if open_count > close_count:
                count_data[i] = 1
                lines = text.split('\n')
                for l in lines:
                    new_offset = l.rfind(brackets[i][0])
                    if new_offset != -1:
                        self.offset = new_offset
            elif open_count < close_count:
                count_data[i] = 2
        logger.debug( 'data: '+str( count_data))
        if 2 in count_data:
            logger.debug( 'paren err')
            self.flags.parenerr = True
        elif 1 in count_data:
            self.flags.contparen = True
        else:
            self.flags.parenerr = False
            self.flags.contparen = False

        #checks for deleted continuation characters (: or \)
        keychars = re.compile(":$|\\\\$",re.M)
        indentchar_count = len(keychars.findall(text))
        logger.debug('indent count: %s', indentchar_count)
        if indentchar_count == 0 and self.flags.continput:
            logger.debug( 'indent del')
            self.flags.continput = False
            

