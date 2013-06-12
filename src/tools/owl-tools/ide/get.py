# tools/user/ide/get.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import gtk, os.path, string, time, logging
import widgets, dialogs

logger = logging.getLogger(__name__)


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        logger.debug('%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0))
        return res
    return wrapper

class EditorBase:

    def get_filedata(self, filename, info, projname=None):
        if filename.startswith('*'):
            filename = filename[1:]
        if projname:
            return self.get_project(projname).files[filename][info]
        if self.project:
            if filename in self.project.files:
                return self.project.files[filename][info]
        if filename in self.noproject.files:
            return self.noproject.files[filename][info]

    def get_project(self,projname):
        if projname == 'No Project':
            return self.noproject
        return self.project

    def get_recent(self):
        self.recent = project.Remembered()

    def get_focus_buffer(self):
        main_window = self.wTree.get_widget("main_window")
        textview = main_window.get_focus()
        try:
            textbuffer = textview.get_buffer()
        except:
            textview = self.get_textview()
            textbuffer = textview.get_buffer()
        return textbuffer, textview


    def get_treeview_selection_names(self):
        """
        gets text of current selection in project tree
        """

        treeselect = self.projectview.get_selection()
        (treestore, treepaths) = treeselect.get_selected_rows()
        filenames = []
        for path in treepaths:
            if len(path) == 1:
                continue
            treeiter = treestore.get_iter(path)
            filenames.append(treestore.get_value(treeiter,0))
        return filenames

    def get_textview_new(self):
        """
        creates and returns a new textview
        """
        textview = widgets.TextView(wrap=self.wrap)
        textbuffer = textview.get_buffer()
        textbuffer.add_selection_clipboard(self.clipboard)
        textbuffer.connect_after('insert-text', self.on_insert_text)
        textbuffer.found_txt = textbuffer.create_tag('found', background = gtk.gdk.Color('#CCCCFF'))

        textview.show()       
        return textview

    def get_tab_name(self, page=-1,get_saved=False):
        """
        gets the text label of the tab at position page
        if get_saved: allows function to be used to determine
        whether the file has been changed since last save
        returns either text of tab label (if get_saved=False)
        or False if get_saved=True and the file has not been saved
        """
        if page == -1:
            page = self.notebook.get_current_page()
        if not page == -1:
            child = self.notebook.get_nth_page(page)
            labelbox = self.notebook.get_tab_label(child)
            tablabel = labelbox.get_children()[0]
            labeltext = tablabel.get_text()
            if labeltext.startswith('*'):
                if get_saved:
                    return False
                return labeltext[1:]
            return labeltext

    def get_textview(self,page=-1):
        """
        gets textview (child widget) of notebook tab at position
        page. If page=-1, gets textview of current tab
        """
        if page==-1:
            page = self.notebook.get_current_page()
        if not page == -1:
            scrollw = self.notebook.get_nth_page(page)
            textview= scrollw.get_child()
            return textview
        

    def get_text_from_tab(self, textview=None, page=None):
        """
        returns a string containing contents of textview
        """
        if page:
            textview = self.get_textview(page)
        textbuffer = textview.get_buffer()
        startiter = textbuffer.get_start_iter()
        enditer = textbuffer.get_end_iter()
        return textbuffer.get_text(startiter, enditer)

    def get_line(self, textbuffer, property_changed):
        if property_changed.name == 'cursor-position':
            pos = textbuffer.get_property('cursor-position')
            textiter = textbuffer.get_iter_at_offset(pos)

            offset = textiter.get_line_offset()
            self.linebar.get_buffer().set_text(' Col: '+str(offset))

def name_from_path(filepath):
    """
    gets the last part of the path: the name of the file
    """
    if filepath is not None:
        path,filename=os.path.split(filepath)
        return filename

@timer
def text_from_file(filepath,show_alert=True):
    """
    returns contents of file at filepath as a string
    if the file is a project, calls open_project() and
    returns False
    if file is empty, returns empty string
    """
    try:
        infile = open(filepath,'r')
    except IOError:
        if show_alert:
            no_file_alert(filepath)
            return
        return ''
    
    if infile:
        text = infile.read()
        infile.close()

        text = string.replace(text, '\r\n', '\n')
        text = string.replace(text, '\r', '\n')

        if not text:
            return ''

        return text

def no_file_alert(filepath):
    alert_dlg = dialogs.ErrorAlert("Could not find file \n\t" +filepath)
    alert_dlg.run()

