#!/usr/bin/env python
# tools/user/ide/gui_gtk.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import gtk, gobject, gtk.glade, xml.etree.ElementTree, gtksourceview2
import sys, re, os, os.path, time, operator, logging, traceback, signal
import string
import threading, Queue
import mcu_ed
import objects, console, dialogs, widgets, get, owlxml, conditions, files
import tempfile, glob

#this is temp fix for problem of gtk warnings ending up on queue
import warnings
warnings.simplefilter('ignore', Warning)

OLD_OUT = sys.stdout
CWD = owlxml.CWD
LAST_PATH = owlxml.LAST_PATH
PREF_PATH = owlxml.PREF_PATH

try:
    os.makedirs(os.curdir+os.sep+'tmp')
except OSError:
    pass

LOG_PATH = os.path.abspath(CWD+'/tmp/owl_ide_log.txt')
if not os.path.isfile(LOG_PATH):
    logfile = open(LOG_PATH, 'w')
    logfile.close()

logging.basicConfig(filename=LOG_PATH,
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Editor(get.EditorBase):

    def __init__(self, queue, events, flags, cond):
        self.wTree = gtk.glade.XML(files.glade())

        main_window = self.wTree.get_widget("main_window")
        #main_window.hide()
        
        main_window.set_icon_from_file(files.icon())

        self.events = events
        self.queue = queue
        self.cond = cond
        self.flags = flags

        self.wrap = False
        
        self.actions_setup()
        self.proj_list = {}
        self.project_setup()
        self.recent_setup()

        self.current_file = None  #name
        self.open_files = {}     #name->project
        self.recent_files = {}   #name->path
        self.ports = set([])

        self.notebook = self.wTree.get_widget("notebook2")
        self.notebook.set_scrollable(True)
        self.clipboard = gtk.Clipboard()
        self.unsaved_count = 0

        self.linebar = self.wTree.get_widget('linebar')

        self.console_tv = None

        self.autoconnect = False
        self.port_name = ''
        #self.set_sensitive_console(False)

        self.preferences = {}
        if os.path.isfile(PREF_PATH):
            self.preferences_setup()
        else:
            self.preferences_dialog(None)            

        if self.notebook.get_n_pages() == 0:
            self.new_file(None)

        pane = self.wTree.get_widget("project_pane")
        pane.connect("notify",self.on_move_pane)
        self.pane_pos = pane.get_property('position')

            
        self.popupmenu_setup()
        self.projectview.connect('button_press_event',self.on_treeview_rightclick)
        

        main_window.present()
        main_window.show_all()

        self.console_tv.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(.42,.42,.42))

        gtk.main()

    def actions_setup(self):
        #set up actions
        main_window = self.wTree.get_widget("main_window")
        main_window.connect('delete-event',self.check_close)
        main_window.connect('destroy',self.close)
        actions = {
            "on_main_window_destroy": gtk.main_quit,
            "on_save_file": self.save_file,
            "on_new_file": self.new_file,
            "on_open_file": self.open_file_dialog,
            "on_open_project": self.open_project,
            "on_save_file_as": self.save_as,
            "on_remove_tab": self.remove_tab,
            "on_change_tab":self.on_change_tab,
            "on_quit":self.close,
            "on_new_project":self.new_project,
            "on_cursor_changed": self.update_current_tab,
            "on_save_project": self.save_project,
            "on_close_project":self.close_project,
            "on_cut": self.cut,
            "on_copy": self.copy,
            "on_paste": self.paste,
            "on_program": self.program,
            "on_run":self.run,
            "on_flash":self.flash_project,
            "toggle_projectpane": self.toggle_projectpane,
            "on_connect": self.connect,
            "on_change_port":self.port_name_dialog,
            "on_toggle_connect": self.toggle_connect,
            "on_clear_console":self.on_clear_console,
            "on_preferences": self.preferences_dialog,
            "on_findreplace": self.find_replace}
        self.wTree.signal_autoconnect(actions)           
                


    def console_setup(self):
        parent = self.wTree.get_widget('scroll_console')
        
        self.console_tv = console.Console(self.queue,
                                           self.events,
                                           self.flags,
                                           self.cond,self.wTree)
        parent.add(self.console_tv)

        parent.show_all()

        if not self.flags.connected:

            textbuffer = self.console_tv.get_buffer()
            textbuffer.begin_not_undoable_action()
            textbuffer.add_selection_clipboard(self.clipboard)
            

            self.console_tv.set_editable(False)
            self.console_tv.set_cursor_visible(False)

        else:
            self.console_tv.initialize()
        


    def project_setup(self):

        self.projectview = self.wTree.get_widget("project_treeview")
        self.projectview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.treestore = widgets.project_setup(self.projectview)

        self.noproject = objects.Project(LAST_PATH,False,
                                         name='No Project')
                                        
        self.noproject.iter = self.treestore.append(None,['No Project', 400])
        
        self.projectview.connect("row-activated",self.open_file_treeview)
        self.project = None

        self.set_sensitive_project(False)


    def on_treeview_rightclick(self, treeview, event):
        """
        treeview context menus: determines which to display
        """
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            selector = treeview.get_selection()
            rows = selector.get_selected_rows()
            row_nums = [i[0] for i in rows[1]]
            path = treeview.get_path_at_pos(x, y)
            #check to see if selection includes both open project and closed project:
            if path is not None: #if no path, ignore
                if row_nums.count(row_nums[0]) != len(row_nums):
                    if 1 in row_nums and self.project:
                        selector.unselect_all()
                        selector.select_path(path[0])
                    else:
                        self.popup_multiproj.popup(None,None,None,event.button, time)
                        return True
                if path[0] not in rows[1]:
                    selector.unselect_all()
                    selector.select_path(path[0])
                a_path = path[0]
                if a_path[0] > 1 or (not self.project and a_path[0]==1):
                    self.popup_proj.popup(None,None,None,event.button, time)
                    return True
                if selector.count_selected_rows() == 1:
                    if len(a_path) > 1:
                        self.popup_one.popup( None, None, None, event.button, time)
                    else:
                        if self.treestore.get_value(self.treestore.get_iter(a_path),0) != 'No Project':
                            self.popup_openproj.popup(None,None,None, event.button, time)
                    return True
                logger.debug('multi')
                self.popup_multi.popup(None,None,None,event.button, time)
                return True
            

    def popupmenu_setup(self):
        """
        creates context menus for treeview
        """
        self.popup_one= widgets.popup_menu(('Open',self.open_file_treeview),
                                        ('Save',self.save_file_treeview),
                                        ('Remove from Project',self.remove_from_project),
                                        ('Close',self.close_tabs_treeview),
                                        ('sep',None),
                                        ('Run',self.run_treeview),
                                        ('Program',self.program_treeview),
                                        ('sep',None),
                                        ('Open All in Project',self.open_all_project),
                                        ('Close Project',self.close_project))
        self.popup_multi = widgets.popup_menu(('Open',self.open_file_treeview),
                                              ('Save', self.save_file_treeview),
                                              ('Remove from Project',self.remove_from_project),
                                              ('Close',self.close_tabs_treeview),
                                              ('sep',None),
                                              ('Program',self.program_treeview),
                                              ('sep',None),
                                              ('Open All in Project',self.open_all_project),
                                              ('Close Project',self.close_project))
        self.popup_openproj = widgets.popup_menu(('Open All',self.open_all_project),
                                             ('Save',self.save_project),
                                             ('Close',self.close_project))
        self.popup_proj = widgets.popup_menu(('Open Project',self.open_proj_treeview),
                                             ('Remove from List',self.remove_proj_from_tree),
                                             ('Program',self.program_proj_treeview))
        self.popup_multiproj = widgets.popup_menu(('Remove from List',self.remove_proj_from_tree))
                                             
        

    def on_move_pane(self, pane, property_changed):
        """ 
        signal handler for user adjusting project pane
        """
        # A widget property has changed.  Ignore unless it is 'position'.
        if property_changed.name == 'position':
            pos = pane.get_property('position')
            if self.pane_pos == 0 and pos != 0:
                self.toggle_projectpane(value=True, set_pos=pos)
            elif pos == 0:
                self.toggle_projectpane(value=False)
            self.pane_pos = pos

    def recent_setup(self):
        """
        gets last opened directory, set of recent files,
        set of recent ports, dict of recent projects and
        their files from xml description
        """
        self.dir = os.getcwd()
        self.remembered = objects.Remembered()
        self.remembered.get()
        self.recent_files = self.remembered.recent
        self.ports = self.remembered.ports
        if self.remembered.dir:
            self.dir = self.remembered.dir
        for projpath in self.remembered.projs:
            self.add_projlist_to_tree(projpath)

    def preferences_dialog(self, widget):
        """
        """
        prefDlg = dialogs.PreferencesDialog(self.preferences)
        result, preferences = prefDlg.run()
        if result == gtk.RESPONSE_OK:
                self.preferences = preferences
                logger.debug('have prefs')
                self.save_preferences()
                logger.debug('save prefs')
                self.change_preferences()
                logger.debug('changed prefs')

    def preferences_setup(self):
        self.preferences, projectpath, self.port_name = owlxml.get_pref()
        if not self.port_name:
            self.port_name = ''
        if projectpath:
            self.open_project(projpath=projectpath)
            
        self.change_preferences()

    def change_preferences(self):
        """
        after preferences have been changed, sets properties accordingly
        problem?: changing preferences sets pane to 200 if show pane is selected, ignoring
        non-default position of open pane
        """
        for pref in self.preferences:
            getattr(self,pref+'_cb')(self.preferences[pref])

    def preference_showprojects_cb(self,value):
        self.toggle_projectpane(widget=None, value=value)

    def preference_autoconnect_cb(self, value):
        self.autoconnect = value
        if not self.console_tv:
            self.console_setup()
            if self.autoconnect and not self.flags.connected:
                self.toggle_connect(value=True)
            elif not self.autoconnect:
                textbuffer = self.console_tv.get_buffer()
                textbuffer.set_text("***Connect board to start***\n")
                self.console_tv.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(.42,.42,.42))
                startiter, enditer = textbuffer.get_bounds()
                textbuffer.apply_tag(self.console_tv.header_txt, startiter, enditer)
        return

    def preference_openlastproject_cb(self,value):
        """does nothing"""
        return

    def preference_autosaveproject_cb(self,value):
        return

    def preference_programconn_cb(self, value):
        return

    def preference_resetalert_cb(self, value):
        return

    def preference_wordwrap_cb(self, value):
        if value == self.wrap:
            return

        self.wrap = value
        if value:
            wrap = gtk.WRAP_WORD
        else:
            wrap = gtk.WRAP_NONE
        for i in xrange(self.notebook.get_n_pages()-1):
            textview = self.get_textview(page=i)
            textview.set_wrap_mode(wrap)
            

    def save_preferences(self):
        """
        saves preferences to xml file,
        preferences: dictionary mapping name of preferences dialog widgets to value
        """
        if self.project:
            name = self.project.path
        else:
            name = LAST_PATH
        owlxml.save_pref(self.preferences, name, self.port_name)


    def save_recent(self):
        self.remembered.recent = self.recent_files
        self.remembered.ports = self.ports
        self.remembered.dir = self.dir
        self.remembered.projs = []
        for proj in self.proj_list:
            self.remembered.projs.append(self.proj_list[proj][0])
        owlxml.save_recent(self.remembered)


    def add_tab_button(self):
        child,add_box, add_label = widgets.add_tab()
        add_label.connect('clicked',self.new_file)
        page = self.notebook.append_page(child,add_box)
        

    def make_page(self, name, textview):
        """
        sets up actual notebook page, including label with close button
        called by new_file or open_file functions
        """
    
        position = self.notebook.get_n_pages() - 1

        scrolltext, labelbox, labelbutton = widgets.make_page(name, textview)
        labelbutton.connect('clicked',self.remove_tab)
        
        self.notebook.append_page(scrolltext, labelbox)
        self.notebook.reorder_child(scrolltext, position)
        self.notebook.set_current_page(position)

        textview.grab_focus()

        textview.get_buffer().connect("modified-changed",self.page_modified,textview)
        textview.get_buffer().connect("notify", self.get_line)


## New_ functions:
        
    def new_file(self, widget):
        """
        drives creation of new file: gets file name and textview, maintains
        open_files, all_files, adds to projectview
        """
        
        first_tab = False
        if self.notebook.get_n_pages() == 0:
            first_tab = True
        
        self.unsaved_count += 1
        name = 'Unsaved File %(count)d'%{'count':self.unsaved_count}

        self.current_file = name

        treeiter = self.treestore.append(self.noproject.iter,[name, 400])
        path = self.treestore.get_path(treeiter)
        new_page = self.notebook.get_n_pages()-1
        if first_tab:
            new_page = 0

        self.open_files[name] = 'No Project'
        self.noproject.add_file(name, None, new_page, path)


        textview = self.get_textview_new()
        self.make_page(name, textview)
        self.set_sensitive_tab(True)
        if first_tab:
            self.add_tab_button()


    def new_project(self, widget):
        """
        drives creation of new project, closes old project, gets
        project name, sets up treestore, adds saved external files to project
        """
        project_path,project_name,self.dir = self.new_project_dialog()
        if not project_path:
            return
        
        if self.project:
            self.close_all()
            
        self.project = objects.Project(project_path, False, project_name,'',{},None)

        self.projectview.get_column(0).set_title(self.project.name)
        self.project.iter = self.treestore.insert(None,1,[self.project.name, 700])
        self.update_proj_treepaths()
        treepath = self.treestore.get_path(self.project.iter)
        self.proj_list[project_name] = [project_path, treepath, []]
        
        for f in self.noproject.files.keys():
            if self.noproject.files[f]['is_open'] and \
            self.noproject.files[f]['path']:
                self.add_to_project(f)


        if self.open_files:
            self.update_paths()
            self.update_pages()

        self.save_project(None)

        self.set_sensitive_project(True)

    def new_project_dialog(self):
        project_dialog = dialogs.ProjectDialog(folder=self.dir)
        result,path, name,folder = project_dialog.run()
        if result == gtk.RESPONSE_OK:
                return path,name,folder
        return None,None,self.dir

## Open_ functions:
    def open_file(self, filename, filepath):
        """ 
        creates a new tab with text from file
        """
        logger.debug(filename)
        text = self.open_check(filename, filepath)
        if text == False:
            return

        page = self.notebook.get_n_pages() - 1
        
        first_tab = False
        if self.notebook.get_n_pages() == 0:
            first_tab = True
            page = 0

        textview = self.get_textview_new()
        same_tab = False

        if self.current_file and not self.get_filedata(self.current_file, 'path'):
            #current file is not in a project, never saved
            if self.notebook.get_current_page() == -1:
                self.notebook.set_current_page(0)
            old_textview = self.get_textview()
            old_text = self.get_text_from_tab(textview=old_textview)

            if old_text == '': #empty unsaved file: overwrite
                textview = old_textview
                same_tab = True
                old_file = self.current_file
                page = self.notebook.get_current_page()

        textview.get_buffer().begin_not_undoable_action()                    
        textview.get_buffer().set_text(text)
        textview.get_buffer().end_not_undoable_action()
        textview.get_buffer().set_modified(False)
        self.current_file = filename

        #adds opened file to tree, project
        proj = self.project
        if not self.project:
            proj = self.noproject
                    

        if filename not in proj.files:
            treeiter = self.add_to_tree(filename)
            treepath = self.treestore.get_path(treeiter)
            proj.add_file(filename, filepath, page, treepath)
        else:
            proj.files[filename]['is_open'] = True
            proj.files[filename]['page'] = page
        self.open_files[filename] = proj.name

        if not same_tab:
            self.make_page(filename, textview)
        else:
            self.remove_from_tree(old_file)
            self.change_tab_label(filename)
            if old_file in self.noproject.files:
                self.noproject.remove_file(old_file)
            del self.open_files[old_file]

        if first_tab:
            self.add_tab_button()

        self.recent_files[self.current_file] = self.get_filedata(self.current_file, 'path')
        
        self.set_sensitive_tab(True)
        self.project_modified = True

        return textview.get_parent()

    def open_check(self, filename, filepath):
        """
        checks conditions to open file:
        is file already open, is there a file with the same name
        already open
        gets the file text
        """
        if filename in self.open_files:
            #not more than one file of same name open at once
            #issue: files w/ same names in different directories
            if self.get_filedata(filename,'path') != filepath:
                if self.same_name_dialog(filename):
                    self.remove_from_project(filenames=[filename])
                else:
                    return False
            else:
                page_num = self.get_filedata(filename,'page')
                self.notebook.set_current_page(page_num)
                return False

        text = get.text_from_file(filepath)
        if text == None: #missing file
            return False

        return text


        
    def open_file_dialog(self, widget=None, filefilter=None,is_project=False):
        """
        runs open file dialog, returns filename and filepath
        """
        if not filefilter:
            filefilter = gtk.FileFilter()
            filefilter.set_name("Files")
            filefilter.add_pattern("*.txt")
            filefilter.add_pattern("*.py")
            filefilter.add_pattern("*.pyw")
            filefilter.add_pattern("*.owl")
            filefilter.add_pattern("*.md")
        allfilter = gtk.FileFilter()
        allfilter.set_name("All Files")
        allfilter.add_pattern("*")
        
        openDlg = dialogs.OpenDialog(filters=[filefilter,allfilter],
                                     recent=self.recent_files, folder=self.dir,
                                     select_multiple=not(is_project))
        
        result, filepaths, folder = openDlg.run()
        if result == gtk.RESPONSE_OK:
            if is_project:
                self.open_project(projpath=filepaths[0])
                self.dir = folder
            else:
                filenames = []
                for path in filepaths:
                    filenames.append(get.name_from_path(path))
                self.dir = folder
                for i in xrange(len(filenames)):
                    self.open_file(filenames[i], filepaths[i])
                
        return None, None

    def open_project_dialog(self):
        filefilter = gtk.FileFilter()
        filefilter.set_name("Project Files")
        filefilter.add_pattern("*.xml")

        return self.open_file_dialog(None,filefilter,True)

    def open_file_treeview(self, widget=None, path=None, view_column=None):
        """
        opens activated file from treeview
        """
        if path:
            if path[0] > 1 or not self.project:
                self.open_proj_treeview()
                return
        filenames = self.get_treeview_selection_names()
        logger.debug(filenames)
        logger.debug(self.project)
        logger.debug(self.projectview.get_selection().get_mode())
        for filename in filenames:
            if filename in self.open_files:
                page_num = self.get_filedata(filename, 'page')
                self.notebook.set_current_page(page_num)
                continue
            filepath = self.get_filedata(filename, 'path')
            if filepath:
                self.open_file(filename, filepath)
                self.update_pages()

    def open_all_project(self,widget):
        """
        opens all files in current project
        """
        for f in self.project.files:
            self.open_file(f, self.project.files[f]['path'])
        self.update_pages()
        

    def open_project(self,widget=None,projpath=''):
        """
        opens project from xml description (string)
        """
        if not projpath:
            projname, projpath = self.open_project_dialog()
        if not projpath:
            return

        if self.close_all(): #closes all files, inc open project and external
            return
        self.projectview.collapse_all()
        
        logger.debug('projpath: %s', projpath)
        if projpath == LAST_PATH:
            proj = self.noproject
            proj.open_from_file()
        else:
            proj = objects.Project(projpath, True)
            if proj.name in self.proj_list:
                self.remove_proj_from_tree(projname=proj.name)
            self.project = proj
            self.projectview.get_column(0).set_title(proj.name)
            try:
                treeiter = self.treestore.get_iter((1,))
                self.treestore.set_value(treeiter, 1, 400)
            except ValueError:
                pass
            proj.iter = self.treestore.insert(None,1,[proj.name, 700])
            treepath = self.treestore.get_path(proj.iter)
            self.proj_list[proj.name] = [proj.path,treepath,proj.get_filepaths()]
            #self.add_projlist_to_tree(name=proj.name, files=proj.files.keys())
        current = proj.current
        page_order = {}
        for f in proj.files:
            treeiter = self.add_to_tree(f)
            treepath = self.treestore.get_path(treeiter)
            proj.files[f]['treepath'] = treepath
            if proj.files[f]['is_open']:
                child = self.open_file(f, proj.files[f]['path'])
                if child:
                    page_order[child] = proj.files[f]['page']
        #reorder pages as they were saved
        numpages = len(page_order)
        for child in page_order:
            if page_order[child] < numpages and page_order[child] > 0:
                self.notebook.reorder_child(child,page_order[child])
        page = self.get_filedata(current, 'page')
        if page is not None:
            self.notebook.set_current_page(page)
        self.update_pages()
        self.update_proj_treepaths()

        #select path
        self.set_sensitive_project(True)
        self.update_paths()

        self.project_modified = False
        

    def open_proj_treeview(self, widget=None):
        """
        opens a project from its listing in the treeview
        """
        treeselect = self.projectview.get_selection()
        (treestore, treepaths) = treeselect.get_selected_rows()
        path = (treepaths[0][0],)
        treeiter = self.treestore.get_iter(path)
        name = self.treestore.get_value(treeiter, 0)
        self.open_project(projpath=self.proj_list[name][0])
        
        return
                

## Save_ functions:
    def save_file(self, widget=None, filename=None):
        """
        drives saving file: checks if previous version exists,
        writes text into new file
        """
        logger.debug('entering save_file, %s', filename)
        if not filename:
            filename = self.current_file
        if filename.startswith('*'):
            filename = filename[1:]
        
        filepath = self.get_filedata(filename, 'path')

                    
        new_file = False #no previous version of file exists
        if not filepath:
            #file is unsaved - set up file, still have to save contents
            new_file = True
            if not self.save_new(): #save canceled
                return

            filename = self.current_file
            filepath = self.get_filedata(filename, 'path')

        if filename not in self.open_files:
            return

        page = self.get_filedata(filename, 'page')
        
        textview = self.get_textview(page)

        #check textview and page:
        child = textview.get_parent()
        check_page = self.notebook.page_num(child)
        if check_page != page:
            print 'ERROR', page, check_page, filename
            raise Exception

        if self.get_tab_name(page=check_page) != filename:
            print 'ERROR', filename, self.get_tab_name(page=check_page)
            raise Exception
        
        textbuffer = textview.get_buffer()
        
        if textbuffer.get_modified() or new_file:
            text = self.get_text_from_tab(textview=textview)
            text = string.replace(text, '\r\n', '\n')
            text = string.replace(text, '\r', '\n')
            outfile = open(filepath,'w')
            outfile.write(text)
            outfile.close
                
        textbuffer.set_modified(False)

        self.recent_files[filename] = filepath

    def save_file_treeview(self, widget):
        """
        saves a file from a treeview context menu option
        """
        filenames = self.get_treeview_selection_names()
        for name in filenames:
            self.save_file(filename=name)

        
    def save_as(self, widget):
        """
        checks if previous version of file exists; if so, saves
        as new file; if not, saves copy: saves to new file, does
        not modify current file
        """
        if not self.get_filedata(self.current_file,'path'):
            self.save_file()
        else:
            filepath, filename, self.dir = self.save_as_dialog()
        if filepath:
            self.save_copy(filepath,filename)
            self.change_tab_label(filename)

    def save_as_dialog(self):
        saveDlg = dialogs.SaveAsDialog(folder=self.dir)
        result, filepath, filename, folder = saveDlg.run()
        if result == gtk.RESPONSE_OK:
            return filepath, filename, folder
        else:
            return None, None, self.dir

    def save_new(self):
        """
        saves file that has no previous saved version
        """
        filepath, filename, self.dir = self.save_as_dialog()
        try:
            if not filepath:
                return False
            proj = self.project
            if not proj:
                proj = self.noproject
            if filename in proj.files:
                if not self.same_name_dialog(filename):
                    return False
                else:
                    self.remove_from_project(filenames=[filename])
                    self.change_tab_label(filename)
            self.remove_from_tree()
            treeiter = self.add_to_tree(filename)
        except Exception, e:
            logger.exception('save failed')
        treepath = self.treestore.get_path(treeiter)
        page = self.get_filedata(self.current_file, 'page')
        proj = self.project
        if not self.project:
            proj = self.noproject
        proj.add_file(filename, filepath, page, treepath)
        self.open_files[filename] = proj.name

        self.noproject.remove_file(self.current_file)
        del self.open_files[self.current_file]
        self.current_file = filename

        self.change_tab_label(filename)
        
        self.update_paths()

        return True

    def save_copy(self, filepath, filename):
        """
        saves contents of current tab in new file, does not save old file
        """
        textview = self.get_textview()
        if not textview:
            return
        text = self.get_text_from_tab(textview=textview)

        proj = self.project
        if not self.project:
            proj = self.noproject
        if filename in proj.files:
            if  self.same_name_dialog(filename):
                self.remove_from_project(filenames=[filename])
            else:
                return

        self.current_file = filename

        treeiter = self.add_to_tree(filename)
        treepath = self.treestore.get_path(treeiter)
        page = self.notebook.get_n_pages() -1

        proj = self.project
        if not self.project:
            proj = self.noproject
        self.open_files[self.current_file] = proj.name
        proj.add_file(self.current_file, filepath, page, treepath)

        textview = self.get_textview_new()
        self.make_page(filename, textview)
        self.notebook.set_current_page(page)

        text = string.replace(text, '\r\n', '\n')
        text = string.replace(text, '\r', '\n')
        outfile = open(self.get_filedata(self.current_file,'path'),'w')
        outfile.write(text)
        outfile.close

        textview.get_buffer().set_text(text)
        self.save_file()
        textview.get_buffer().set_modified(False)

    def save_project(self,widget=None):
        """
        saves xml description of project to current working directory
        """
        if not self.project: #no project to save
            if not self.preferences['preference_openlastproject']:
                return
            else:
                logger.debug('saving externals')
                self.noproject.save()
                self.save_preferences()
        else:
            for f in self.project.files:
                self.save_file(filename=f)
            self.project.save()
            self.set_sensitive_project(True)
            self.save_preferences()
            self.project_modified = False

    def same_name_dialog(self, filename):
        if self.project and filename in self.project.files:
            alert = dialogs.SameNameDialog(filename, self.project.name)
        else:
            alert = dialogs.SameNameDialog(filename)
        result = alert.run()

        if result == gtk.RESPONSE_OK:
            return True
        return False
        
        

##Other functions
    ##add, remove, or change information in notebook and treeview

    def on_change_tab(self, notebook, page_notusable, page_num):
        """
        maintains editor data concerning current file inc tree selection
        """
        try:  #checks for add tab button
            child = self.notebook.get_nth_page(page_num)
            if child.get_text() == 'add tab':
                self.notebook.stop_emission('switch-page')
              
        except:
        
            if self.notebook.get_n_pages == 2:
                return
            if not self.open_files:
                return
            self.current_file = self.get_tab_name(page_num)
            self.update_tree_selection()
            
        if self.project:
            if self.current_file in self.project.files:
                self.project.current = self.current_file
            else:
                self.noproject.current = self.current_file
        else:
            self.noproject.current = self.current_file
            
        self.project_modified = True


    def remove_tab(self, widget=None, page=-1, filename=None):
        """
        removes tab: widget should indicate which if called by button
        if called by close_all, page given
        """
        logger.debug('remove: page: %s, name: %s',page,filename)
        if widget:
            if type(widget) != gtk.MenuItem:
                filename = widget.get_name() #name of tab to be removed
                page = self.get_filedata(filename, 'page')

        elif not filename:
            filename = self.get_tab_name(page)
        else:
            page = self.get_filedata(filename,'page')

        if filename == '':
            return
        if not self.is_saved(filename):
            result = self.confirm_save([filename],'file','close')
            if result == 'Stop':
                return True

        if filename in self.noproject.files:
            self.remove_from_tree(filename)
            self.noproject.remove_file(filename)
        else:
            self.get_project(self.open_files[filename]).close_file(filename)
            treepath = self.get_filedata(filename, 'treepath')
            self.treestore.set_value(self.treestore.get_iter(treepath), 0, filename)
            
        del self.open_files[filename]

        if self.notebook.get_n_pages() == 2: # if only real tab left
            self.notebook.remove_page(1)
            self.notebook.remove_page(0)
            self.current_file = ""
            self.set_sensitive_tab(False)
        else:
            self.notebook.remove_page(page)
        self.update_pages()
        self.update_paths()
        self.project_modified = True

    def close_tabs_treeview(self, widget):
        """
        handles close tab option from treeview popup menu:
        can close multiple files
        """
        filenames = self.get_treeview_selection_names()
        for filename in filenames:
            if filename in self.open_files:
                if self.remove_tab(filename=filename):
                    return True


    def add_to_project(self, filename):
        """
        adds filename to project entry in Project, treeview
        paths: [treepath, filepath]
        """

        self.remove_from_tree(filename)
        filepath = self.noproject.files[filename]['path']
        page = self.noproject.files[filename]['page']
        treepath = self.noproject.files[filename]['treepath']
        
        self.project.add_file(filename, filepath, page, treepath)
        self.open_files[filename] = self.project.name
        self.noproject.remove_file(filename)
        
        if filename in self.open_files:
            self.open_files[filename] = self.project.name
            
        self.add_to_tree(filename)
        self.project_modified = True

    def remove_from_project(self, widget=None, filenames=None):
        """
        takes a list of filenames and removes them from the project
        if a file is external files (no project), does not remove from
        project object as that is done by self.remove_tab
        otherwise, removes the file from the project object, and the treeview
        """
        if not filenames:
            filenames = self.get_treeview_selection_names()

        for filename in filenames:
            if filename.startswith('*'):
                filename = filename[1:]

            if filename in self.noproject.files:
                page = self.get_filedata(filename, 'page', 'No Project')
                if self.remove_tab(None,page):
                    return True
                continue
                
            if filename in self.project.files:
                page = self.get_filedata(filename, 'page', self.project.name)
                if self.get_filedata(filename, 'is_open', self.project.name):
                    if self.remove_tab(None,page):
                        return True
                self.remove_from_tree(filename)
                self.project.remove_file(filename)
        
        self.project_modified = True
        
    def close_project(self, widget):
        """
        closes currently opened project: saves state and closes all tabs,
        clears projectview
        """
        if self.project_modified:
            result = self.confirm_save([], 'project', 'close')
            if result == 'Stop':
                return True
        if self.project:
            self.projectview.get_column(0).set_title('No Project')
            treeiter = self.treestore.get_iter((1,))
            self.treestore.set_value(treeiter, 1, 400)
            #closes open project files:
            for name in self.project.files:
                if self.project.files[name]['is_open']: #if file is open
                    page = self.project.files[name]['page']
                    if self.remove_tab(None,page):
                        return True
                    self.update_pages()
            self.project = None
            self.update_paths()
            if self.notebook.get_n_pages == 1:
                self.set_sensitive_tab(False)
            self.set_sensitive_project(False)


    def close_all(self):
        """
        closes project + all opened external files
        """
        if self.project:
            if self.close_project(None):
                return True
        for i in xrange(self.notebook.get_n_pages()-1):
            if self.remove_tab(None, i):
                return True

        if self.open_files:
            self.update_paths()
        

    def close(self, widget, event=None):
        """
        on destroy window
        """
        #check for unsaved files: all open, not just current
        logger.debug('entering gui_gtk.close')
        try:
            logger.debug(str(self.events))
            logger.debug(str(self.flags))
            self.toggle_connect(False)
            self.save_recent()
            self.save_preferences()
            if self.preferences['preference_autosaveproject']:
                self.save_project()
            elif self.project_modified and self.project:
                self.confirm_save([], 'project', 'close')
            result = self.confirm_save(self.open_files.keys(), 'file', 'close')
            if result == 'Stop':
                return True
            if self.preferences['preference_autosaveproject'] or \
               (self.preferences['preference_openlastproject'] and not self.project):
                self.save_project()
        finally:
            gtk.main_quit()
            self.events.destroy.set()
            logger.debug('leaving close')

        
    def check_close(self, widget=None, event=None):
        if not self.flags.cmddone and self.events.inputdone.is_set():
            result = self.disconn_msg()
            return result

    def confirm_save(self, filenames ,savetype, event):
        """
        launches dialog to ask user whether to save:
        filenames: if saving files, must be a list of existing filenames
                    if saving project, not used
        savetype: 'file' for saving files, 'project' for saving project
        event: action by user that requires save: 'run', 'quit'
        """
        if savetype=='file':
            saved = False
            for name in filenames:
                if not self.is_saved(name):
                    save_alert = dialogs.SaveAlert(savetype,event)
                    result = save_alert.run(name)
                    if result == 0:
                        return 'Stop'
                    elif result == 1:
                        self.save_file(filename=name)
                        saved = True
            return saved
                        
        elif savetype=='project':
            save_alert = dialogs.SaveAlert(savetype,event)
            result = save_alert.run(self.project.name)
            if result == 0:
                return 'Stop'
            elif result == 1:
                self.save_project()
            else:
                #if event == 'run':
                return False
        return True
        

    def add_to_tree(self, filename):
        """
        adds name to project treeview: only saved files to project row
        """
        if self.project:
            parent_iter = self.project.iter
        else:
            parent_iter = self.noproject.iter
        treeiter = self.treestore.append(parent_iter,[filename, 400])
        return treeiter

    def add_projlist_to_tree(self, projpath='', name='', files=[]):
        """
        adds project data to the treeview, intended for unopened projects
        """
        if not name:
            name, files = owlxml.get_project_list(projpath)
        if name:
            if name not in self.proj_list:
                treeiter = self.treestore.append(None, [name, 400])
                treepath = self.treestore.get_path(treeiter)
                self.proj_list[name] = [projpath, treepath, files.values()]
                for f in files:
                    self.treestore.append(treeiter, [f, 400])
            
        

    def remove_from_tree(self, filename=''):
        """
        removes filename from tree, when unsaved file is saved
        or external file is closed
        """
        if not filename:
            filename = self.current_file
    
        treepath = self.get_filedata(filename, 'treepath')
    
        treeiter = self.treestore.get_iter(treepath)
        self.treestore.remove(treeiter)

        self.update_paths()

    def remove_proj_from_tree(self, widget=None, projname=''):
        if self.project and self.project.name == projname:
            return
        if not projname:
            treeselect = self.projectview.get_selection()
            (treestore, treepaths) = treeselect.get_selected_rows()

            #if selection includes multiple projects, only consider project headings
            row_nums = [i[0] for i in treepaths]
            if row_nums:
                if row_nums.count(row_nums[0]) != len(row_nums):
                    treepaths = filter(lambda x: len(x)==1,treepaths)
                else:
                    treepaths = [treepaths[0][0]]
            projnames = []
            for path in treepaths:
                treeiter = self.treestore.get_iter(path)
                projnames.append(self.treestore.get_value(treeiter, 0))
        else:
            projnames = [projname]
        for name in projnames:
            treepath = self.proj_list[name][1]
            treeiter = self.treestore.get_iter(treepath)
            self.treestore.remove(treeiter)
            del self.proj_list[name]
            self.update_proj_treepaths()

    def change_tab_label(self, label, textview=None, saved=None):
        """
        changes the text of the tab's label to label
        uses current tab by default, or tab containing textview if specified
        if saved is specified (True or False): adds or removes * from label
        """
        if not textview:
            page = self.notebook.get_current_page() 
            child = self.notebook.get_nth_page(page)
        else:
            child = textview.get_parent()
        labelbox = self.notebook.get_tab_label(child)
        tablabel = labelbox.get_children()[0]
        if saved is not None:
            filename = tablabel.get_text()
            if filename.startswith('*'):
                filename = filename[1:]
            if not saved:
                label = label + filename
            else:
                label = filename
            treepath = self.get_filedata(filename,'treepath')
            if treepath:
                treeiter = self.treestore.get_iter(treepath)
                self.treestore.set_value(treeiter, 0, label)
        if not label:
            return
        tablabel.set_text(label)

        if saved != False:
            tabbutton = labelbox.get_children()[1]
            tabbutton.set_name(label)

    #get functions

    def is_saved(self, filename):
        """
        checks if file is saved or not, replacing
        textview.get_modified as that is unreliable
        """
        if filename not in self.open_files:
            return False
        page = self.get_filedata(filename, 'page')
        result = self.get_tab_name(page, True)
        if result:
            return True
        return False
        


    def on_insert_text(self, textbuffer, textiter, text, length):
        """
        handles autoindent for editor: replaces gtksourceview2 autoindent
        for correct column count, consistent indent
        """
        mark = textbuffer.create_mark('mark',textiter)
        textbuffer.handler_block_by_func(self.on_insert_text)

        if text == '\n':

            textiter = textbuffer.get_iter_at_mark(mark)
            line = textiter.get_line()
            start = textbuffer.get_iter_at_line(line-1)
            end = textbuffer.get_iter_at_mark(textbuffer.get_insert())
            newline = textbuffer.get_text(start, end)
            
            indent = self.autoindent(textbuffer, newline)
            if newline.endswith(':\n'):
                end = textbuffer.get_iter_at_mark(textbuffer.get_insert())
                textbuffer.insert(end,'    ')

            brackets = (('(',')'),('[',']'),('{','}'))
            offset = 0
            last_offset = textbuffer.get_iter_at_mark(textbuffer.get_insert()).get_offset()
            closed_paren = False
            
            for i in xrange(3):
                open_count = newline.count(brackets[i][0])
                closed_count = newline.count(brackets[i][1])
                if open_count - closed_count > 0:
                    new_offset = newline.rfind(brackets[i][0])
                    if new_offset > offset:
                        offset = new_offset
                elif closed_count - open_count > 0:
                    closed_paren = True
                    end = textbuffer.get_iter_at_mark(textbuffer.get_insert())
                    text = textbuffer.get_text(textbuffer.get_start_iter(), end)
                    old_offset = text.rfind(brackets[i][0])
                    if old_offset < last_offset:
                        last_offset = old_offset
                        bracket = brackets[i][0]
            if offset:
                indent = textbuffer.get_iter_at_mark(textbuffer.get_insert()).get_line_offset()
                offset = offset - indent
                end = textbuffer.get_iter_at_mark(textbuffer.get_insert())
                textbuffer.insert(end, ' '*(offset+1))
            if closed_paren:
                textiter = textbuffer.get_iter_at_offset(last_offset)
                start = textbuffer.get_iter_at_line(textiter.get_line())
                end = textbuffer.get_iter_at_line(textiter.get_line())
                end.forward_to_line_end()
                oldline = textbuffer.get_text(start,end)
                offset = ''
                while oldline and oldline[0].isspace():
                    offset += oldline[0]
                    oldline = oldline[1:]
                indent = len(offset)
                enditer = textbuffer.get_iter_at_mark(textbuffer.get_insert())
                if indent > enditer.get_line_offset():
                    textbuffer.handler_unblock_by_func(self.on_insert_text)
                    self.get_textview().scroll_mark_onscreen(textbuffer.get_insert())
                    return
                indentiter = textbuffer.get_iter_at_line_offset(line+1, indent)
                textbuffer.delete(indentiter, enditer)
            self.get_textview().scroll_mark_onscreen(textbuffer.get_insert())
        textbuffer.handler_unblock_by_func(self.on_insert_text)
        return

    def autoindent(self,textbuffer, text):
        """ 
        finds indent after newline, returns 
        """
        if not text:
            return

        if text.endswith('\n'):
            #removes trailing newline
            text = text[:-1]

        offset = ''
        while text and text[0].isspace():
            offset += text[0]
            text = text[1:]
        indent = len(offset.expandtabs())
        end = textbuffer.get_iter_at_mark(textbuffer.get_insert())
        
        textbuffer.insert(end,offset)
        return indent

            

    def page_modified(self, textbuffer, textview):
        """     
        when the page_modified signal is emitted from a textbuffer in an editor
        tab, changes tab label and scrolls if necessary
        """
        if textbuffer.get_modified():
            self.change_tab_label('*',textview, saved=False)
            textview.scroll_mark_onscreen(textbuffer.get_insert())
            if self.project:
                self.project_modified = True
        else:
            self.change_tab_label('',textview, saved=True)




    #update functions

    def update_paths(self):
        """ 
        iterates through project treeview, gets each child iter and updates
        corresponding path
        """
        self.update_project_paths('No Project')
        if self.project:
            self.update_project_paths(self.project.name)


    def update_project_paths(self, project_name):
        """
        iterates through an individual project,
        project name is either self.project or 'No Project'
        """
        if project_name == 'No Project':
            parent_iter = self.noproject.iter
        elif project_name == self.project.name:
            parent_iter = self.project.iter
        else:
            return

        #should be iter pointing to first child
        treeiter = self.treestore.iter_children(parent_iter)
        if treeiter:
            self.update_single_path(treeiter, project_name)
            while self.treestore.iter_next(treeiter):
                treeiter = self.treestore.iter_next(treeiter)
                self.update_single_path(treeiter, project_name)


    def update_single_path(self, treeiter, projname):
        """
        updates path for one file, from treeiter
        """
        filename = self.treestore.get_value(treeiter,0)
        if filename.startswith('*'):
            filename = filename[1:]
        proj = self.get_project(projname)
        proj.files[filename]['treepath'] = self.treestore.get_path(treeiter)

    def update_pages(self):
        """
        updates page entry in open_files for each file
        """
        logger.debug(self.open_files)
        logger.debug(self.project)
        if self.notebook.get_n_pages():
            for i in xrange(self.notebook.get_n_pages()-1):
                name = self.get_tab_name(i)
                if name:
                    projname = self.open_files[name]
                    proj = self.get_project(projname)
                    proj.files[name]['page'] = i

    def update_proj_treepaths(self):
        try:
            treeiter = self.treestore.get_iter((1,))
        except ValueError:
            return
        treeiter = self.treestore.iter_next(treeiter)
        while treeiter:
            projname = self.treestore.get_value(treeiter, 0)
            treepath = self.treestore.get_path(treeiter)
            self.proj_list[projname][1] = treepath
            treeiter = self.treestore.iter_next(treeiter)
    
    def update_current_tab(self, widget):
        """
        sets current tab from treeview selection
        """
        filenames = self.get_treeview_selection_names()
        if len(filenames) == 1:
            if filenames[0].startswith('*'):
                filenames[0] = filenames[0][1:]
            if filenames[0] in self.open_files:
                page_num = self.get_filedata(filenames[0],'page')
                self.notebook.set_current_page(page_num)

    def update_tree_selection(self):
        """
        sets tree selection from current file
        """
        treepath = self.get_filedata(self.current_file, 'treepath')
        self.projectview.expand_to_path(treepath)
        treeselect = self.projectview.get_selection()
        treeselect.unselect_all()
        treeselect.select_path(treepath)        
    
#toggle button sensitivity
    def set_sensitive_tab(self, sensitive):
        """
        sets sensitivity of button related to files,
        based on whether a file is open: sensitive=True makes
        menu and toolbar options clickable
        """
        tab_widgets = ['menu_save', 'texttoolbar_save', 'menu_save_as']
        for widget_name in tab_widgets:
            widget = self.wTree.get_widget(widget_name)
            widget.set_sensitive(sensitive)


    def set_sensitive_project(self, sensitive):
        """
        sets sensitivity of button related to projects,
        based on whether a project is open: sensitive=True makes
        menu and toolbar options clickable
        """
        project_widgets = ['save_project', 'close_project', 'project_save',
                           'project_flash', 'project_close']
        for widget_name in project_widgets:
                widget = self.wTree.get_widget(widget_name)
                widget.set_sensitive(sensitive)


    def set_sensitive_console(self, widget, value):
        """
        sets sensitivity of buttons on console toolbar,
        main menu, and context menus
        """

        console_names = ['console_program',
                               'console_run',
                               'clear_console',
                               'check_connect',
                               'menu_program',
                               'menu_run',
                               'menu_changeport',
                               'project_flash']
        for wname in console_names:
            widget = self.wTree.get_widget(wname)
            widget.set_sensitive(value)
        popup_items = []
        popup_items += self.popup_one.get_children()
        popup_items += self.popup_multi.get_children()
        popup_items += self.popup_proj.get_children()
        popup_items += self.popup_openproj.get_children()
        for widget in popup_items:
            if widget.get_name() in ['Run', 'Program']:
                widget.set_sensitive(value)

#IO

    def connect(self, widget=None):
        """
        connects to the board
        return True if connected successfully, False otherwise
        """

        logger.debug('entering gui_gtk.connect')
        objects.clear_all(self.events, self.flags)
            
        if not self.port_name:
            result = self.port_name_dialog()
            if not result:
                return

        self.mThread = threading.Thread(target=mcu_ed.connect,
                                   args=(self.port_name, self.queue,
                                         self.events,self.flags, self.cond),
                                   name='mcu')
        #self.mThread.daemon = True
        self.mThread.start()
        
        logger.debug('waiting tryconnect')
        self.events.tryconnect.wait()
        logger.debug('have tryconnect, checking conn %s', self.flags.connected)
        if not self.flags.connected:
            self.connect_alert(msg=conditions.get_from_q(self.queue))
            return False

        self.console_tv.connect('quit-signal',self.toggle_connect)
        self.console_tv.connect('conn-fail', self.connect_alert)
        self.console_tv.connect('reset-alert', self.disconn_msg)
        self.console_tv.connect('crash', self.close)
        self.console_tv.connect('in-cmd',self.set_sensitive_console)

        if not self.console_tv.initialize():
            self.flags.connected = False
            return

        tvbuffer = self.console_tv.get_buffer()
        
        self.console_tv.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))

        startiter = tvbuffer.get_start_iter()
        #tvbuffer.insert(startiter, old_text)
        self.console_tv.grab_focus()

        startiter, enditer = tvbuffer.get_bounds()

        previter = tvbuffer.get_iter_at_line(enditer.get_line()-1)
        tvbuffer.remove_all_tags(startiter, previter)
        tvbuffer.apply_tag(self.console_tv.header_txt, startiter, previter)
        
        tvbuffer.apply_tag(self.console_tv.not_editable, startiter, enditer)

        self.console_tv.set_editable(True)
        self.console_tv.set_cursor_visible(True)

        tvbuffer.place_cursor(enditer)
        enditer = tvbuffer.get_end_iter()
        self.console_tv.scroll_mark_onscreen(tvbuffer.get_insert())


        
        logger.debug('leaving gui_gtk.connect')

        return True

    def port_name_dialog(self, widget=None):
        """
        if no port name can be found or Owl...Change Port is selected:
        launches dialog to get port name from user
        """
        autoconnect_initial = self.autoconnect
        portDialog = dialogs.ComPortDialog(self.port_name, self.autoconnect)
        result, portname, autoconnect = portDialog.run()

        if result == gtk.RESPONSE_OK:
            self.port_name = portname
            self.ports.add(portname)
            self.autoconnect = autoconnect
            
            self.save_preferences()
            return True
        


    def disconnect(self, widget=None):
        """
        disconnects from board, greys out console
        """
        logger.debug('entering gui_gtk.disconnect')
        self.flags.disconnect = True
        self.events.startloop.set()
        logger.debug('connclose waiting')
        self.console_tv.set_editable(False)

        self.events.connclose.wait()

        #self.mThread.join() #still unsure about this one

        start, end = self.console_tv.get_buffer().get_bounds()
        self.console_tv.get_buffer().remove_all_tags(start, end)
        self.console_tv.get_buffer().apply_tag(self.console_tv.header_txt,
                                                start, end)


        disconnect_msg = "\n***board has been disconnected***\n\n"
        
        self.console_tv.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(.42,.42,.42))
        self.console_tv.set_cursor_visible(False)
        self.console_tv.set_editable(False)

        self.console_tv.writer.set_tag(self.console_tv.header_txt)
        print >>self.console_tv.writer, disconnect_msg,
        

        #self.set_sensitive_console(False)

        #while not self.queue.empty():
        #    self.queue.get()

        #objects.clear_all(self.events, self.flags)

        logger.debug('check threads: %s',threading.enumerate())
        self.flags.connected = False
        self.flags.cmddone = True
        
        logger.debug('leaving disconnect')

    def toggle_connect(self, widget=None, value=None):
        """
        handles connecting and disconnecting from board:
        if value=True, connects; otherwise disconnects
        """
        logger.debug('toggle connect %s', value)
        if widget:
            try:
                value = widget.get_active()
            except AttributeError, e:
                pass
        logger.debug('toggling: %s, %s', value, self.flags.connected)
        if value:
            if not self.flags.connected:
                result = self.connect()
                if not result:
                    value = False
                    label = 'Connect'
                else:
                    label = 'Disconnect'
            else:
                label = 'Disconnect'
        else:
            if self.flags.connected:
                self.disconnect()
            label = 'Connect'

        console_widgets = ['console_toggle_connect', 'check_connect']

        for w_name in console_widgets:
            w = self.wTree.get_widget(w_name)
            w.handler_block_by_func(self.toggle_connect)
            try:
                w.handler_block_by_func(self.console_tv.kill)
            except:
                pass
            try:
                w.set_active(value)
            except:
                w.set_active(int(bool(value)))
            w.handler_unblock_by_func(self.toggle_connect)
            try:
                w.handler_unblock_by_func(self.console_tv.kill)
            except:
                pass
            w.set_label(label)
        self.console_tv.emit_stop_by_name('quit-signal')



    def connect_alert(self, widget=None, msg=''):
        """
        launches alert dialog if unable to connect to board
        """
        logger.debug('connect alert!')
        try:
            writer = objects.Writable(self.console_tv)
            #print >>writer, msg
        except AttributeError:
            pass
        if msg.startswith('device reports'): #reset in linux while running
            if not self.preferences['preference_resetalert']:
                print >>writer, 'Connection reset'
                return
        print >>writer, 'Unable to connect!'
        alertdialog = dialogs.ConnectAlert()
        stop_autoconnect = alertdialog.run(self.autoconnect, msg)
        if stop_autoconnect:
            self.autoconnect = False
            self.preferences['preference_autoconnect'] = False
            self.save_preferences()
        self.console_tv.emit_stop_by_name('conn-fail')

    def disconn_msg(self, widget=None):
        """
        warns the user that they have killed the connection unsafely,
        must reset board
        """
        if os.name == 'nt':
            msg = 'The program is still running!\n\nDisconnecting ' \
                'the board now will not\nclose the connection correctly.' \
                '\n\nYou must reset the board TWICE before\ntrying to ' \
                'connect again. If you still can\'t\nconnect, restart the' \
                ' editor and try again.'
        else:
            msg = 'The program is still running!\n\nDisconnecting ' \
                'the board now will not\nclose the connection correctly.' \
                '\n\nPlease press the reset button on the board, then\n' \
                'try to exit again.'
        alertdialog = dialogs.WarningAlert(msg, os.name)
        result = alertdialog.run()
        self.console_tv.emit_stop_by_name('reset_alert')
        return result


    def on_clear_console(self, widget):
        """
        clears old console commands: hides but does not delete command history
        ie, up arrow still finds commands from current session, whether cleared or not
        does not reset board
        """
        if self.flags.connected:
            self.toggle_connect(value=False)
            self.console_tv.get_buffer().set_text('')
            self.toggle_connect(value=True)

        else:
            self.console_tv.get_buffer().set_text('***board has been disconnected***\n')
    
    def program(self, widget=None, filepaths=None):
        """
        loads a program or programs
        if filepaths (list of full file paths), uses that list
        to populate dialog list, otherwise default is project files
        """
        logger.debug('entering gui_gtk.program')
        if not self.port_name:
            self.port_name_dialog()
        
        c_writer = objects.Writable(self.console_tv)
        c_writer.set_tag(self.console_tv.program_txt)

        if self.flags.connected:
            self.toggle_connect(value=False)
            print >>c_writer, 'Please reset the board!'

        if not filepaths:
            filepaths = self.program_dialog()
        if not filepaths:
            logger.debug('leaving program: no filenames')
            return
        
        for f in filepaths:
            name = get.name_from_path(f)
            if name in self.open_files:
                result = self.confirm_save([name], 'file', 'program')
                if result == 'Stop':
                    return
        for f in filepaths:
            if remove_tabs(f):
                return

        if not self.reset_alert():
            return

        logger.debug(self.flags)


        p_writer = objects.ProgWriter()
        logger.debug('mcu:')

        objects.clear_all(self.events, self.flags)
        conditions.get_from_q(self.queue)
        time.sleep(.8)   #allows connection time to close correctly   
        mThread = threading.Thread(target=mcu_ed.programList,
                                   args = (self.port_name,
                                           [p_writer]+filepaths,
                                           self.queue,
                                           self.events,
                                           self.flags),
                                   name = 'pro')
        mThread.start()
        
        if not self.events.tryconnect.wait(5):
            self.connect_alert(msg='Connection timed out: please reset the board.')
            return
        if self.flags.serialerr:
            logger.debug('checking serialerr')
            self.connect_alert(msg=conditions.get_from_q(self.queue))
            return
        if not self.events.outputinq.wait(8):
            self.connect_alert(msg='Connection write failed: connected successfully\n' \
                                    'but attempt to write timed out.\n\nPlease reset the ' \
                                    'board and restart the application.')
            
            sys.stdout = OLD_OUT
            return
        self.events.outputinq.clear()
        if self.flags.serialerr:
            self.connect_alert(msg='Failed to connect!')
        result = conditions.get_from_q(self.queue)
        logger.debug('result: %s',result)
        if result:
            print >>c_writer, result
            logger.debug('consoleready set')
            self.events.consoleready.set()
            if self.flags.err:
                logger.debug('waiting outputinq')
                self.events.outputinq.wait()
                c_writer.set_tag(self.console_tv.err_txt)
                print >>c_writer, conditions.get_from_q(self.queue)
         
    
    
        if self.flags.disconnect and self.flags.connected:
            self.toggle_connect(value=False)
        
        if self.preferences['preference_programconn']:
            logger.debug('program autoconnecting')
            self.toggle_connect(value=True)
        logger.debug('leaving program')
        return

    def program_treeview(self, widget):
        filenames = self.get_treeview_selection_names()
        filepaths = []
        for filename in filenames:
            path = self.get_filedata(filename, 'path')
            if not path:
                page = self.get_filedata(filename, 'page','No Project')
                result = self.confirm_save([filename],'file','program')
                if result == 'Stop':
                    return
                if result:
                    filename = self.get_tab_name(page)
                    path = self.get_filedata(filename, 'path')
            if path:
                filepaths.append(path)
        self.program(filepaths=filepaths)

    def program_proj_treeview(self, widget):
        treeselect = self.projectview.get_selection()
        (treestore, treepaths) = treeselect.get_selected_rows()
        path = (treepaths[0][0],)
        treeiter = self.treestore.get_iter(path)
        name = self.treestore.get_value(treeiter, 0)
        filepaths = self.proj_list[name][2]
        self.program(filepaths=filepaths)

    def program_dialog(self):
        """
        launches dialog for user to choose which files should be programmed
        """
        files = {}
        
        proj = self.project
        if not self.project:
            proj = self.noproject
        
        current_file = proj.current
        logger.debug(proj)
        logger.debug(proj.current)
        
        for f in proj.files:
            files[f] = proj.files[f]['path']
            
        programDialog = dialogs.ProgramDialog(current_file,files,self.dir)
        
        filenames, self.dir = programDialog.run()
        
        return filenames

    def run(self, widget=None, filename=None):
        """ 
        creates a command to run current file on the board
        """
        if not filename:
            filename = self.current_file
            
        result = self.confirm_save([filename],'file','run')
        if result == 'Stop':
            return True
        if filename.startswith('*'):
            filename = filename[1:]
            
        filepath = self.get_filedata(filename, 'path')

        if not self.flags.connected:
            self.toggle_connect(value=True)

        if self.flags.connected:
            try:
                self.console_tv.on_key_press(None, None, 'run '+filepath)
            except TypeError:
                dialogs.ErrorAlert('Error opening file!\n\nPlease make sure that ' \
                           'file has been saved.').run()
                return
        return

    def run_treeview(self, widget):
        filename = self.get_treeview_selection_names()[0]
        
        self.run(filename=filename)

    def reset_alert(self):
        msg = 'Please reset the board!\n\nYou cannot program '\
              'the board until\nafter you have pressed the reset button.' \
              '\n\nAfter you have pressed the reset button,\n check OK ' \
              'to continue.'
        if os.name != 'nt':
            msg += '\n\nIf you cannot close this message,\npress the reset button again to cancel\nprogramming.'
        logger.debug('reset alert')
        resetdlg = dialogs.WarningAlert(msg)
        result = resetdlg.run()

        return not result

    def flash_project(self, widget):
        if not self.project:
            proj = self.noproject
        else:
            proj = self.project

        filenames = []
        for f in proj.files:
            filenames.append(proj.files[f]['path'])

        self.program(None, filenames)

    def cut(self, widget):
        textbuffer, textview = self.get_focus_buffer()
        textbuffer.cut_clipboard(self.clipboard,True)

    def copy(self, widget):
        textbuffer, textview = self.get_focus_buffer()
        textbuffer.copy_clipboard(self.clipboard)

    def paste(self, widget):
        textbuffer, textview = self.get_focus_buffer()
        textbuffer.paste_clipboard(self.clipboard,None,True)


    def find_replace(self, widget):
        finddlg = dialogs.FindReplaceDialog()
        textbuffer, textview = self.get_focus_buffer()
        is_console = False
        if textview.get_name() == 'console':
            is_console = True
        finder = objects.FindReplace(textview)
        response = finddlg.run(is_console)
        for r in response:
            finder.respond(r)
        finder.clear_highlight()        
        


    def toggle_projectpane(self, widget=None, value=None, set_pos=None):
        pane_widgets = ['menu_check_showprojects', 'project_hide']
        hpane = self.wTree.get_widget("project_pane")
        if widget:
            value = widget.get_active()
        
        if set_pos:
            hpane.set_position(set_pos)
        else:
            if value:
                hpane.set_position(200)
            else:
                hpane.set_position(0)
                
        for w_name in pane_widgets:
            w = self.wTree.get_widget(w_name)
            w.set_active(value)


def run(overrule=False):
    try:
        tempdir = tempfile.gettempdir()
        if glob.glob(tempdir + '\owlide*') and not overrule:
            logger.debug("already exists, exiting")
            dialogs.ErrorAlert('The editor is already running!').run()
            sys.exit()            

        else:
            lockfile = tempfile.NamedTemporaryFile(prefix='owlide')
 


            try:

                queue = Queue.Queue()
                events = objects.Events()
                flags = objects.Flags()
                cond = threading.Condition(threading.RLock())

                eThread = threading.Thread(target=Editor,
                                           args=(queue, events, flags, cond),
                                           name = 'ed')
                eThread.start()

                events.destroy.wait()
                os.kill(os.getpid(),signal.SIGTERM)
             
            except Exception:
                logging.exception('mainthread failed')
                
                #sys.exit()
    except SystemExit:
        pass
    else:
        print >>OLD_OUT, traceback.format_exc()

        
def remove_tabs(filename):
    '''
    replaces tabs with spaces in python file, for mcu
    '''
    try:
        pyfile = open(filename, 'r')
        pytext = pyfile.read()
        pyfile.close()
    except:
        dialogs.ErrorAlert('Error opening file!\n\nPlease make sure that ' \
                           'file has been saved').run()
        return True

    pytext = pytext.replace('\t', '    ')

    pyfile = open(filename, 'w')
    pyfile.write(pytext)
    pyfile.close()

    
