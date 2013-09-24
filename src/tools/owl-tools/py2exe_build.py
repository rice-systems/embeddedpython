# tools/user/setup.py
#
# disttools script to build .exe on Win32 platforms.
#
# Copyright 2013 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

from distutils.core import setup
import py2exe
import os
import sys

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

setup(
    name = 'owlide',
    description = 'Owl IDE',
    version = '0.1',

    windows = [
                  {
                      'script': 'owlide',
                      'icon_resources': [(0, "ide/owl.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': 'cairo, pango, pangocairo, atk, gobject, gio'
                  }
              },

    data_files=[
                   'ide/projecttree.glade',
                   'ide/owl.png',
                   'ide/owl.ico',
                   'drivers/owl.inf',
                   # If using GTK+'s built in SVG support, uncomment these
                   os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                   os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
               ]
)

