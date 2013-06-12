# tools/user/ide/widgets.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import gtk, gtksourceview2, pango

class TextView(gtksourceview2.View):
    def __init__(self,viewtype='editor',wrap=False):
        textbuffer = Buffer()
        gtksourceview2.View.__init__(self,textbuffer)

        lm = gtksourceview2.LanguageManager()
        pylang = lm.get_language('python')
        textbuffer.set_data('language-manager', lm)
        textbuffer.set_language(pylang)

        self.set_auto_indent(False)
        self.set_indent_on_tab(True)
        self.set_tab_width(4)
        self.set_indent_width(self.get_tab_width())
        fontdesc = pango.FontDescription("monospace")
        self.modify_font(fontdesc)
        self.not_editable = self.get_buffer().create_tag('not_editable', editable=False)
        if wrap:
            self.set_wrap_mode(gtk.WRAP_WORD)
        else:
            self.set_wrap_mode(gtk.WRAP_NONE)
        self.set_insert_spaces_instead_of_tabs(True)
            
        if viewtype == 'editor':
            self.set_show_line_numbers(True)
            textbuffer.set_max_undo_levels(-1)
        elif viewtype == 'console':
            styles = gtksourceview2.StyleSchemeManager()
            #style = styles.get_scheme('oblivion')
            #textbuffer.set_style_scheme(style)
            textbuffer.set_max_undo_levels(0)

        textbuffer.connect('insert-text', self.scroll_to)


    def scroll_to(self, tvbuffer, textiter, text, textlen):
        self.scroll_mark_onscreen(tvbuffer.get_insert())


class Buffer(gtksourceview2.Buffer):
    def __init__(self):
        gtksourceview2.Buffer.__init__(self)

        self.set_max_undo_levels(10)


def popup_menu(*menu_items):
    popup = gtk.Menu()
    coord = 0
    for (label, handler) in menu_items:
        if label == 'sep':
            popup.attach(gtk.SeparatorMenuItem(),0,1,coord,coord+1)
            coord += 1
        else:
            widget = gtk.MenuItem(label)
            widget.connect('activate',handler)
            widget.set_name(label)
            popup.attach(widget,0,1,coord,coord+1)
            coord += 1
    popup.show_all()
    return popup
        
        
def add_tab():
    """
    creates fake notebook tab to act as new tab button
    """

    add_box = gtk.HBox()
    add_txt = gtk.Label('')
    add_label = gtk.Button()
    add_box.pack_start(add_txt)
    add_box.pack_start(add_label)
    add_label.set_relief(gtk.RELIEF_NONE)
    labelimg = gtk.Image()
    labelimg.set_from_stock(gtk.STOCK_ADD,gtk.ICON_SIZE_MENU)
    x,y = gtk.icon_size_lookup_for_settings(labelimg.get_settings(), gtk.ICON_SIZE_MENU)
    labelimg.set_size_request(x+2,y+2)
    add_label.set_image(labelimg)
    add_label.show_all()
    
    add_label.set_name('add_label')

    child = gtk.Label('add tab')
    child.show()
    return child, add_box, add_label

def make_page(name, textview):
    #set up label:
    labelbox = gtk.HBox()
    labeltext = gtk.Label(name)
    labelbutton = gtk.Button()
    labelbutton.set_relief(gtk.RELIEF_NONE)
    labelimg = gtk.Image()

    labelimg.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_MENU)
    labelbutton.set_image(labelimg)

    style = gtk.RcStyle()
    style.xthickness = 0
    style.ythickness = 0
    labelbutton.modify_style(style)

    labelbutton.set_name(name)
    labelbox.pack_start(labeltext)
    labelbox.pack_start(labelbutton)
    labelbox.show_all()

    scrolltext = gtk.ScrolledWindow()
    scrolltext.add(textview)
    scrolltext.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    scrolltext.show_all()

    return scrolltext, labelbox, labelbutton

def project_setup(treeview):

    treestore = gtk.TreeStore(str, int)
    treeview.set_model(treestore)

    cell = gtk.CellRendererText()
    tv_column = gtk.TreeViewColumn('No Project', cell)
    tv_column.add_attribute(cell, 'text',0)
    tv_column.add_attribute(cell, 'weight',1)
    treeview.append_column(tv_column)


    return treestore

