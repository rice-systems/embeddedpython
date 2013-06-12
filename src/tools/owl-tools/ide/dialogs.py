# tools/user/ide/dialogs.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import gtk, gtk.glade, gobject, sys, os, connection
import files
GLADE_FILE = "projecttree.glade"
old_out = sys.stdout

ICON_FILE = "icon.svg"

class DialogBase:
    def __init__(self, dlg_name):
        self.wTree = gtk.glade.XML(files.glade(),dlg_name)
        self.dlg = self.wTree.get_widget(dlg_name)
        
        self.dlg.set_icon_from_file(files.icon())

        self.dlg.connect('key-press-event', self.on_key_press)

    def on_key_press(self, widget, event):
        if event.keyval == 65293:
            try:
                if type(self.dlg.get_focus()) != gtk.Button:
                    ok = self.wTree.get_widget('ok')
                    ok.activate()
                    return True
            except:
                pass


class SaveAsDialog(DialogBase):
    def __init__(self,filename="", folder=''):
        DialogBase.__init__(self, "save_as_dialog")
        self.filename = filename
        self.dir = folder
        

    def run(self):
        self.dlg.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)

        if self.filename:
            self.dlg.set_current_name(self.filename)
        elif self.dir:
            self.dlg.set_current_folder(self.dir)

        result = self.dlg.run()
        if not result:
            self.dlg.destroy()
            return None, None, None, None

        filepath = self.dlg.get_filename()
        if filepath:
            self.dir, self.filename = os.path.split(filepath)
       
            self.dlg.destroy()

        return result, filepath, self.filename, self.dir
        

class OpenDialog(DialogBase):
    def __init__(self, filename="", filters=[], recent={}, folder='~',
                 select_multiple=True):
        DialogBase.__init__(self, "open_dialog")
        self.filename = filename
        self.filters = filters
        self.recent = recent
        self.dir = folder
        self.select_multiple = select_multiple

    def run(self):
        vbox = self.wTree.get_widget('open_vbox')

        liststore = gtk.ListStore(gobject.TYPE_STRING)
        self.combobox = gtk.ComboBoxEntry(liststore)
        
        self.combobox.set_text_column(0)
        self.combobox.show()
        vbox.pack_start(self.combobox, expand=False, fill=False)

        box_entries = sorted(self.recent)
        for entry in box_entries:
            self.combobox.append_text(entry)
        
        self.combobox.connect('changed',self.combo_select)

        self.dlg.set_current_folder(self.dir)
        self.dlg.set_select_multiple(self.select_multiple)

        self.dlg.unselect_all()
        
        for f in self.filters:
            self.dlg.add_filter(f)

        self.result = self.dlg.run()

        self.filepaths = self.dlg.get_filenames()

        self.current_folder = self.dlg.get_current_folder()

        self.dlg.destroy()
        
        return self.result, self.filepaths, self.current_folder

    def combo_select(self, widget):
        filename = self.combobox.get_active_text()
        if filename in self.recent:
            filepath = self.recent[filename]
            self.dlg.set_filename(filepath)
        else:
            self.dlg.set_filename(filename)
        

class SaveAlert(DialogBase):
    def __init__(self, savetype, event):
        DialogBase.__init__(self, "save_alert")
        self.savetype = savetype
        self.event = event

    def run(self, name):            
        if self.event == 'close' and self.savetype=='file':
            event_msg = 'closing the tab?'
        elif self.event == 'close' and self.savetype=='project':
            event_msg = 'closing the project?'
        elif self.event == 'run':
            event_msg = 'running the program?'
        elif self.event == 'program':
            event_msg = 'programming this file?'

        else:
            event_msg = ''

        textbox = self.wTree.get_widget("savequit_alert")
        self.dlg.realize()
        color = self.dlg.get_style().copy().bg[gtk.STATE_NORMAL]
        textbox.modify_base(gtk.STATE_NORMAL, color)
        textbuffer = textbox.get_buffer()
        textbuffer.set_text("You have not saved this " + self.savetype + ": \n\t"\
                            + name + "\nDo you want to save before " + event_msg)
        
        self.result = self.dlg.run()

        self.dlg.destroy()
        return self.result


class ProjectDialog(DialogBase):

    def __init__(self,projectname="",folder='~'):
        DialogBase.__init__(self, "new_project_dialog")
        self.projectname = projectname
        self.dir = folder
        self.projectpath = ''

    def run(self):

        filefilter = gtk.FileFilter()
        filefilter.set_name("Project Files")
        filefilter.add_pattern("*.xml")
        allfilter = gtk.FileFilter()
        allfilter.set_name("All Files")
        allfilter.add_pattern("*")

        self.dlg.add_filter(filefilter)
        self.dlg.add_filter(allfilter)

        self.dlg.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)

        if self.projectname:
            self.dlg.set_current_name(self.projectname)
        elif self.dir:
            self.dlg.set_current_folder(self.dir)

        self.result = self.dlg.run()

        if self.result == gtk.RESPONSE_OK:
            self.projectpath = self.dlg.get_filename()
            self.dir, self.projectname = os.path.split(self.projectpath)
            if not self.projectpath.endswith('.xml'):
                self.projectpath += '.xml'

        self.dlg.destroy()

        return self.result, self.projectpath, self.projectname, self.dir


class PreferencesDialog(DialogBase):

    def __init__(self,preferences):
        DialogBase.__init__(self, "preferences_dialog")
        self.options = ['preference_showprojects',
                        'preference_autoconnect',
                        'preference_openlastproject',
                        'preference_autosaveproject',
                        'preference_programconn',
                        'preference_resetalert',
                        'preference_wordwrap']
        if preferences:
            self.preferences = preferences
        else:
            self.preferences = {}
            for opt in self.options:
                self.preferences[opt] = False
        self.opt_widgets = []

    def run(self):

        for option in self.options:
            self.opt_widgets.append(self.wTree.get_widget(option))
        for widget in self.opt_widgets:
            widget.set_active(self.preferences[widget.get_name()])
        
        self.result = self.dlg.run()

        for widget in self.opt_widgets:
            self.preferences[widget.get_name()] = widget.get_active()

        self.dlg.destroy()
        return self.result, self.preferences


class SameNameDialog(DialogBase):
    def __init__(self, filename, project=None):
        DialogBase.__init__(self, "same_name_dialog")

        self.filename = filename
        self.project = project

    def run(self):

        textbox = self.wTree.get_widget("same_name_alert")
        self.dlg.realize()
        color = self.dlg.get_style().copy().bg[gtk.STATE_NORMAL]
        textbox.modify_base(gtk.STATE_NORMAL, color)
        textbuffer = textbox.get_buffer()
        if self.project:
            place_description = "' in " + self.project
        else:
            place_description = "' opened"
        
        textbuffer.set_text("There is already a file named '" + self.filename \
                         + place_description + ".\n\nDo you want to replace the older file?")
        
        self.result = self.dlg.run()

        self.dlg.destroy()

        return self.result


class ComPortDialog(DialogBase):
    def __init__(self,portname='',autoconnect=False):
        DialogBase.__init__(self, "comport_dialog")
        self.portname = portname
        self.autoconnect = autoconnect

    def run(self):
        name_entry = self.wTree.get_widget('port_entry').child
        name_entry.set_text(self.portname)
        name_entry.grab_focus

        name_entry.connect('key-press-event',self.on_key_press)

        check_autoconnect = self.wTree.get_widget('check_autoconnect')

        check_autoconnect.set_active(self.autoconnect)

        autodetect = self.wTree.get_widget('autodetect')
        autodetect.connect('clicked',self.on_autodetect)

        result = self.dlg.run()

        self.autoconnect = check_autoconnect.get_active()
        self.portname = name_entry.get_text()

        self.dlg.destroy()

        return result, self.portname, self.autoconnect


    def on_autodetect(self, widget):
        try:
            self.portname = connection.autodetect()
            name_entry = self.wTree.get_widget('port_entry').child
            name_entry.set_text(self.portname)
        except Exception,e:
            
            msg = "Could not detect serial port automatically!"
            noautodlg = ErrorAlert(msg)
            noautodlg.run()
            widget.set_sensitive(False)


class WarningAlert(DialogBase):
    def __init__(self, msg, osname=None):
        DialogBase.__init__(self, "warning_alert")
        self.msg = msg
        self.win = None
        if osname:
            if osname == 'nt':
                self.win = True
            else:
                self.win = False

    def run(self):
        textbox = self.wTree.get_widget('alert_msg')
        textbox.get_buffer().set_text(self.msg)
        self.dlg.realize()
        color = self.dlg.get_style().copy().bg[gtk.STATE_NORMAL]
        textbox.modify_base(gtk.STATE_NORMAL, color)
        self.dlg.connect('key-press-event', self.on_key_press)
        if self.win==False:
            cancel = self.wTree.get_widget('cancel')
            cancel.set_label('Force Quit')
        result = self.dlg.run()
        self.dlg.destroy()

        if self.win != False:
            if result == 1:
                return False
            return True
        else:
            if result == 1:
                return True
            return False
       

            
class ErrorAlert(DialogBase):
    def __init__(self, msg):
        DialogBase.__init__(self, "error_alert")
        self.msg = msg
        
    def run(self):
        textbox = self.wTree.get_widget('alert_msg')
        textbox.get_buffer().set_text(self.msg)
        self.dlg.realize()
        color = self.dlg.get_style().copy().bg[gtk.STATE_NORMAL]
        textbox.modify_base(gtk.STATE_NORMAL, color)
        self.dlg.run()
        self.dlg.destroy()
            
class ConnectAlert(DialogBase):
    def __init__(self):
        DialogBase.__init__(self, "connect_alert")

    def run(self,autoconnect, msg):

        textbox = self.wTree.get_widget('textview1')
        self.dlg.realize()
        color = self.dlg.get_style().copy().bg[gtk.STATE_NORMAL]
        textbox.modify_base(gtk.STATE_NORMAL, color)

        
        self.checkbutton = self.wTree.get_widget('check_autoconnect')
        self.checkbutton.set_active(not autoconnect)

        if msg:
            msgview = self.wTree.get_widget('error_message')
            msgview.set_visible(True)
            textbox = self.wTree.get_widget('textview2')
            textbox.modify_base(gtk.STATE_NORMAL, color)
            textbox.set_visible(True)
            msgview.get_buffer().set_text(msg)

        self.dlg.run()

        autoconnect = self.checkbutton.get_active()

        self.dlg.destroy()

        return autoconnect

class ProgramDialog(DialogBase):
    def __init__(self, current_file=None, files={},folder='~'):
        DialogBase.__init__(self, "program_dialog")
        self.current_file = current_file
        self.files = files
        self.dir = folder

        actions = {
            "on_browse":self.browse,
            "on_remove": self.remove
            }

        self.wTree.signal_autoconnect(actions)           


    def run(self):

        self.filelist = self.wTree.get_widget('filelist')
        self.filestore = self.get_liststore(self.filelist)
        self.treeselection = self.filelist.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)

        self.combostore = gtk.ListStore(gobject.TYPE_STRING)
        combobox = gtk.ComboBox(self.combostore)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 0)
        combobox.show()
        vbox = self.wTree.get_widget('vbox1')
        vbox.pack_start(combobox, expand=False, fill=False)
        self.combo_dict = {}
        for f in self.files:
            comboiter = self.combostore.append([f])
            combopath = self.combostore.get_path(comboiter)
            self.combo_dict[f] = gtk.TreeRowReference(self.combostore,
                                                      combopath)

            self.filestore.append([f])
        combobox.set_active(0)
        self.combobox = combobox

        result = self.dlg.run()

        self.dlg.destroy()
        if result == gtk.RESPONSE_OK:

            main_file = combobox.get_active_text()
            filenames = [self.files[main_file]]
            newiter = self.filestore.get_iter_first()
            while newiter:
                name = self.filestore.get(newiter,0)
                if name[0] != main_file:
                    filenames.append(self.files[name[0]])
                newiter = self.filestore.iter_next(newiter)
            return filenames, self.dir
        return None, self.dir

    def get_liststore(self, treeview):
        model = gtk.ListStore(gobject.TYPE_STRING)
        treeview.set_model(model)

        self.textrender = gtk.CellRendererText()
        col = gtk.TreeViewColumn('File', self.textrender, text=0)
        
        treeview.append_column(col)

        return model
    

    def browse(self, widget):
        filechooser = FileBrowser(self.dir)
        filenames, self.dir = filechooser.run()
        for f in filenames:
            name = get_name_from_path(f)
            self.files[name] = f
            comboiter = self.combostore.append([name])
            combopath = self.combostore.get_path(comboiter)
            self.combo_dict[name] = gtk.TreeRowReference(self.combostore,
                                                      combopath)
            self.filestore.append([name])
        if filenames:
            if self.combobox.get_active() == -1:
                self.combobox.set_active(0)


    def remove(self, widget):
        model, pathlist = self.treeselection.get_selected_rows()
        reflist = []
        for path in pathlist:
            reflist.append(gtk.TreeRowReference(model, path))
        for ref in reflist:
            treeiter = model.get_iter_from_string(str(ref.get_path()[0]))
            name = self.filestore.get_value(treeiter, 0)
            self.filestore.remove(treeiter)
            comboref = self.combo_dict[name]
            comboiter = self.combostore.get_iter_from_string(
                str(comboref.get_path()[0]))
            self.combostore.remove(comboiter)
        if self.combobox.get_active() == -1:
            self.combobox.set_active(0)

def get_name_from_path(filepath):
    try:
        path,filename=os.path.split(filepath)
        return filename
    except:
        return ''

        

class FileBrowser(DialogBase):
    def __init__(self, folder):
        DialogBase.__init__(self, "open_dialog")
        filefilter = gtk.FileFilter()
        filefilter.set_name("Files")
        filefilter.add_pattern("*.py")
        filefilter.add_pattern("*.owl")
        filefilter.add_pattern("*.md")
        allfilter = gtk.FileFilter()
        allfilter.set_name("All Files")
        allfilter.add_pattern("*")
        self.filters = [filefilter, allfilter]
        self.dir = folder

    def run(self):
        filenames = []
        self.dlg.set_select_multiple(True)
        self.dlg.unselect_all()
        self.dlg.set_current_folder(self.dir)

        for f in self.filters:
            self.dlg.add_filter(f)

        result = self.dlg.run()

        self.current_folder = self.dlg.get_current_folder()

        if result == gtk.RESPONSE_OK:
            filenames = self.dlg.get_filenames()
            
        self.dlg.destroy()
        return filenames, self.current_folder


class FindReplaceDialog(DialogBase):
    def __init__(self):
        DialogBase.__init__(self, "find_dialog")
        self.find_entry = self.wTree.get_widget("find_entry")
        self.find_entry.get_buffer().connect('deleted-text', self.find_text_changed)
        self.find_entry.get_buffer().connect('inserted-text', self.find_text_changed)
        self.replace_entry = self.wTree.get_widget("replace_entry")
        self.dlg.realize()
        color = self.dlg.get_style().copy().bg[gtk.STATE_NORMAL]
        for textview_name in ('textview1','textview2'):
            textview = self.wTree.get_widget(textview_name)
            textview.modify_base(gtk.STATE_NORMAL, color)
        self.opts = ('case_check', 'up_check', 'regex_check', 'highlight_check')
        self.wTree.get_widget('highlight_check').connect('toggled',self.highlight_toggled)
        self.wTree.get_widget('case_check').set_active(True)


    def run(self, is_console, find_text='', replace_text=''):
        self.find_entry.grab_focus()

        if is_console:
            self.wTree.get_widget('replace_all').set_sensitive(False)
        response = 0
        if find_text:
            self.find_entry.set_text(find_text)
        if replace_text:
            self.replace_entry.set_text(replace_text)

        while response != -4:
            response = self.dlg.run()
        
            opt_data = {}
            for widget_name in self.opts:
                widget = self.wTree.get_widget(widget_name)
                opt_data[widget_name] = widget.get_active()

            find_text = self.find_entry.get_text()
            replace_text = self.replace_entry.get_text()
            yield (response, find_text, replace_text, opt_data)

        
        self.dlg.destroy()
        return

    def highlight_toggled(self, widget):
        self.dlg.response(0)

    def on_key_press(self, widget, event):
        if event.keyval == 65293:
            if type(self.dlg.get_focus()) != gtk.Button:
                ok = self.wTree.get_widget('find_next')
                ok.activate()
                return True

    def find_text_changed(self, entrybuffer, pos, chars='', n_chars=0):
        if self.wTree.get_widget('highlight_check').get_active():
            self.dlg.response(0)
