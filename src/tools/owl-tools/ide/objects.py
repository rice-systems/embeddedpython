# tools/user/ide/objects.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import owlxml, threading, re, time, logging, conditions
logger = logging.getLogger(__name__)


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        logger.debug('%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0))
        return res
    return wrapper


class Project:
    def __init__(self, path, from_file, name='',
                 current='', files={}, treeiter=None):
        """
        stores attributes of a project in the ide
        project must have a path
        if from_file=True, attempts to get project data
        from xml file at path
        otherwise, sets project data to input values

        files is a dictionary whose keys are file names
        whose values are dictionaries with keys 'path',
        'page', 'is_open', and 'treepath'
        """
        self.path = path
        
        if not from_file:
            self.name = name
            self.current = current
            self.files = files
            self.iter = treeiter

        else:
            try:
                (self.name, self.current,
                    self.files) = owlxml.get_project(path)
                self.iter = None
            except TypeError:
                self.name = name
                self.current = current
                self.files = files
                self.treeiter = treeiter
                
                
    def add_file(self, filename, filepath, page, treepath):
        self.files[filename] = {'path':filepath, 'page':page,
                                'is_open':True, 'treepath':treepath}

    def remove_file(self, filename):
        del self.files[filename]
        
    def open_file(self, filename):
        self.files[filename]['is_open'] = True

    def close_file(self, filename):
        self.files[filename]['is_open'] = False
        self.files[filename]['page'] = -1

    def save(self):
        owlxml.save_project(self)

    def get_filepaths(self):
        filepaths = []
        for f in self.files:
            filepaths.append(self.files[f]['path'])
        return filepaths
    
    def open_from_file(self):  
        try:              
            (self.name, self.current,
            self.files) = owlxml.get_project(self.path)
        except:
            pass
        
    def __str__(self):
        return self.name + ': ' + str(self.files)


class Remembered:
    """
    stores names and paths of recently saved files,
            names of recently used ports,
            name of last opened directory
    saves to xml file to be recovered at start up
    """
    def __init__(self, recent={}, ports=set([]), directory='', projs=[]):
        self.recent = recent
        self.ports = ports
        self.dir = directory
        self.projs = projs

    def get(self):
        try:
            recent, ports, directory, projs = owlxml.get_recent()
        except:
            return self.recent, self.ports, self.dir, self.projs
        self.recent = recent
        self.ports = ports
        self.dir = directory
        self.projs = projs



class Writable(object):
    """
    handles printing to console:
    appends text to console
    keeps console scrolled to new input
    can apply one tag to new input
    """
    def __init__(self, textview):
        """
        textview must be gtk.TextView
        """
        self.tv = textview
        self.tvbuffer = textview.get_buffer()
        self.tag = None

    def write(self, text):
        """
        appends text to Writeable's textbuffer
        applies self.tag if exists, scrolls to insert
        """
        if self.tag:
            self.tvbuffer.insert_with_tags(self.tvbuffer.get_end_iter(), 
                                    text, self.tag )
                        
        else:
            self.tvbuffer.insert(self.tvbuffer.get_end_iter(), text)
        self.tvbuffer.place_cursor(self.tvbuffer.get_end_iter())
        self.tv.scroll_mark_onscreen(self.tvbuffer.get_insert())

    def set_tag(self, tag):
        """
        applies tag to all text written until
        new tag is set or clear_tag is called
        """
        self.tag = tag

    def clear_tag(self):
        """
        sets self.tag to None: text will be
        written without any additional tags applied
        until a new tag is set
        """
        self.tag = None

class ProgWriter:

    def __init__(self):
        self.contents = ''

    def write(self, text):
        self.contents += text

    def clear(self):
        self.contents = ''


class qWriter:
    def __init__(self, cond, queue, events, flags, err=False):
        self.cond = cond
        self.q = queue
        self.events = events
        self.flags = flags
        self.err = err

    def write(self,text):
        if self.err:
            self.flags.err = True
        logger.debug(text)
        conditions.make_item(self.cond, self.q, item=text)
        self.events.outputinq.set()


class Flags:
    def __init__(self):
        self.disconnect = False #disconnect event from within mcu thread
        self.err = False #console is in exception, should print results as such
        self.connected = False #console is connected
        self.continput = False #console expects more input: from \ or :
        self.contparen = False #console expects more input: open bracket(s)
        self.parenerr = False #unbalanced brackets should result in syntax error
        #(this catches bug in compiler)
        self.cmddone = True #input command has been fully carried out:
        #output is complete; is true when not running a command
        self.serialerr = False #connection has been lost or interrupted
        self.promptset = False

    def clear_all(self):
        self.__init__()
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name in ['disconnect', 'cmddone', 'connected', 'serialerr','promptset']:
            logger.debug('%s set to %s', name, value)

    def __str__(self):
        return 'disconnect : %s\n' \
               'connected : %s\n' \
               'cmddone : %s\n' \
               'serialerr : %s\n' % \
               (self.disconnect,
                self.connected, self.cmddone,
                self.serialerr)
        


class Events:
    def __init__(self):
        self.destroy = threading.Event() #main window destroyed, also general quit signal
        self.tryconnect = threading.Event() #set when attempt to connect has been made
        self.inputdone = threading.Event() # input is complete, command can
        #be checked and run; also used as timer when programming board
        self.outputinq = threading.Event() #an item is in the queue and ready to
        #be printed to the console
        self.consoleready = threading.Event() #output has been printed and
        #the console is ready for more output
        self.startloop = threading.Event() #next iteration of while loop in
        #ipm.run() can begin: previous command is finished
        self.connclose = threading.Event() #set when conn.close is called from ipm,
        #disconnect does not proceed until set
        self.getheader = threading.Event() #console header message can be gathered
        self.haveheader = threading.Event() #console header message has been gathered

    def get_all(self):
        return set([self.destroy,
                self.tryconnect,
                self.inputdone,
                self.outputinq,
                self.consoleready,
                self.startloop,
                self.connclose,
                self.getheader,
                self.haveheader])

    def __str__(self):
        return 'inputdone : %s\n' \
               'outputinq : %s\n' \
               'consoleready : %s\n' \
               'startloop : %s\n' % \
               (self.inputdone.is_set(),
                self.outputinq.is_set(),
                self.consoleready.is_set(),
                self.startloop.is_set())

def clear_all(events, flags):
    for event in events.get_all():
        event.clear()
    flags.clear_all()


class FindReplace:
    """
    handles response from FindReplace dialog:
    given a textview, finds and replaces input strings
    or regular expressions
    """
    def __init__(self, textview):
        """
        returns a FindReplace object for textview
        """
        self.find_text = ''
        self.replace_text = ''
        self.opt_data = {}
        self.textview = textview
        self.tvbuffer = textview.get_buffer()
        self.find_changed= False
        self.finder_regex = None
        self.finder_index = None
        self.search_down = True
        self.occurrences = 0
        self.pattern = None


    def respond(self, response):
        """
        handles response from Find/Replace dialog:
        response: (response_id, find_text, replace_text, opt_data)
        response_id: integer id of user's action
        opt_data: flags corresponding to Find/Replace options
        """
        self.find_changed = self.find_text != response[1]
        if self.opt_data:
            if self.opt_data['case_check'] != response[3]['case_check']:
                self.find_changed = True
        self.find_text = response[1]
        self.replace_text = response[2]
        self.opt_data = response[3]

        if self.opt_data['regex_check'] or not self.opt_data['case_check']:
            self.regex = True
            if not self.finder_regex or self.find_changed:
                self.finder_regex = self.get_finder()
                self.occurrences = len(self.finder_regex)
        else:
            self.regex = False
            self.finder_regex = None
            self.occurrences = 0
            

        if (response[0]==3 and self.opt_data['up_check']) or \
           (response[0]==4 and not self.opt_data['up_check']) or \
           (response[0] != 3 and response[0] != 4 and not self.opt_data['up_check']):
            self.search_down = True
        elif (response[0]==3 and not self.opt_data['up_check']) or \
             (response[0]==4 and self.opt_data['up_check']) or \
             (response[0] != 3 and response[0] != 4 and self.opt_data['up_check']):
            self.search_down = False
            
        if response[0] == 0:
            if self.opt_data['highlight_check']:
                if self.find_changed:
                    self.clear_highlight()
                self.find_all()
            else:
                self.clear_highlight()

        elif response[0] == 1:
            self.replace()

        elif response[0] == 2:
            self.replace_all()

        elif response[0] == 3 or response[0] == 4:
            self.find(True, True)

    def get_finder(self):
        """
        when regular expressions are in use, finds beginning and
        ending indices of all pattern matches in the textview
        """
        if not self.find_text:
            return []
        try:
            if not self.opt_data['case_check']:
                self.pattern = re.compile(self.find_text,re.IGNORECASE)
            else:
                self.pattern = re.compile(self.find_text)
        except: #ignore illegal regular expressions
            return []
            

        start, end = self.tvbuffer.get_bounds()
        text = self.tvbuffer.get_text(start, end)

        insert = self.tvbuffer.get_iter_at_mark(self.tvbuffer.get_insert())
        insert_offset = insert.get_offset()
        end_offset = self.tvbuffer.get_end_iter().get_offset()
        self.finder_index = None

        finder_regex = []
        iters = (self.pattern.finditer(text, insert_offset, end_offset),
                    self.pattern.finditer(text, 0, insert_offset))
        for i in iters:
            finder_regex += [match.span() for match in i]

        return finder_regex              
        

    def find(self, scrollto=False, allow_loop=False, insert=None):
        """
        finds and selects a single instance of find_text in the textview:
        scrollto: flag when set True causes textview to scroll to match
        allow_loop: allows search to restart at the beginning of the textview
        if no match is found
        insert: (find_normal only): starting point for search, cursor location
        by default
        """
        #if self.opt_data['regex_check'] or not self.opt_data['case_check']:
        if not self.find_text:
            return None, None
        if self.regex:
            match_start, match_end = self.find_re()
        else:
            if not insert:
                insert = self.tvbuffer.get_iter_at_mark(self.tvbuffer.get_insert())
            match_start, match_end = self.find_normal(insert, allow_loop)

        if match_start:
            if self.search_down:
                self.tvbuffer.select_range(match_end, match_start)
            else:
                self.tvbuffer.select_range(match_start, match_end)
            if scrollto:
                self.textview.scroll_mark_onscreen(self.tvbuffer.get_insert())

            return match_start, match_end
        return None, None
             
    def find_normal(self, start, allow_loop = False):
        """
        finds and selects a single occurce of find_text, without
        regualr expressions
        """
        if self.search_down:
            found = start.forward_search(self.find_text,0,None)
        else:
            found = start.backward_search(self.find_text,0,None)

        if found:
            return found[0], found[1]

        if allow_loop:
            if self.search_down:
                start = self.tvbuffer.get_start_iter()
                found = start.forward_search(self.find_text,0,None)
            else:
                start = self.tvbuffer.get_end_iter()
                found = start.backward_search(self.find_text,0,None)

            if found:
                return found[0], found[1]

        return None, None
        
    def find_re(self):
        """
        finds a single occurrent of find_text using regular expressions
        """
        if not self.finder_regex:
            return None, None
        if self.finder_index == None:
            if self.search_down:
                self.finder_index = 0
            else:
                self.finder_index = -1
        else:
            if self.search_down:
                self.finder_index += 1
                if self.finder_index >= self.occurrences:
                    self.finder_index = 0
            else:
                self.finder_index -= 1
                if abs(self.finder_index) > self.occurrences:
                    self.finder_index = self.occurrences-1
    
            
        start_offset, end_offset = self.finder_regex[self.finder_index]
        startiter = self.tvbuffer.get_iter_at_offset(start_offset)
        enditer = self.tvbuffer.get_iter_at_offset(end_offset)
        return startiter, enditer

    def find_all(self):
        """
        finds and highlights all instances of find_text in the textview
        """
        cursor_iter = self.tvbuffer.get_iter_at_mark(self.tvbuffer.get_insert())
        if self.regex:
            for match in self.finder_regex:
                start = self.tvbuffer.get_iter_at_offset(match[0])
                end = self.tvbuffer.get_iter_at_offset(match[1])
                self.tvbuffer.apply_tag(self.tvbuffer.found_txt, start, end)
        else:
            found = self.find(False, False, self.tvbuffer.get_start_iter())
            while found[0]:
                self.tvbuffer.apply_tag(self.tvbuffer.found_txt, found[0], found[1])
                found = self.find(False, False)
        self.tvbuffer.place_cursor(cursor_iter)

    def replace(self):
        """
        replaces next find_text with replace_text
        """
        if not self.replace_text:
            return False
        find_next = True
        bounds = self.tvbuffer.get_selection_bounds()
        if bounds:
            text = self.tvbuffer.get_text(bounds[0], bounds[1])
            if text == self.find_text:
                find_next = False

        if find_next:
            start, end = self.find(True, True)
        else:
            start, end = bounds

        if start:
            if not start.has_tag(self.textview.not_editable):
                self.tvbuffer.delete_selection(True, True)
                insert = self.tvbuffer.get_iter_at_mark(self.tvbuffer.get_insert())
                self.tvbuffer.insert(insert, self.replace_text)
                self.tvbuffer.select_range(insert, end)
                return True
        return False

    def replace_all(self):
        """
        replaces all instances of self.find_text with self.replace_text
        does not respect editability of textview and so is not
        availible when textview is console
        """
        start, end = self.tvbuffer.get_bounds()
        text = self.tvbuffer.get_text(start, end)
        if self.regex:
            if self.pattern:
                new_text = self.pattern.sub(self.replace_text,text)
                self.tvbuffer.set_text(new_text)
        else:
            new_text = text.replace(self.find_text, self.replace_text)
            self.tvbuffer.set_text(new_text)    
        

    def clear_highlight(self):
        """
        removes highlighting of found text
        """
        start, end = self.tvbuffer.get_bounds()
        self.tvbuffer.remove_tag(self.tvbuffer.found_txt, start, end)

        
