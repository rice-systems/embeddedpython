# tools/user/setup.py
#
# disttools script to build command line package.
#
# Copyright 2013 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

from distutils.core import setup
import sys
from version import VERSION

# Owl absolutely, positively requires 2.7
if not ((2, 7) <= sys.version_info < (3,)):
    print "Owl requires Python 2.7. Exiting."
    sys.exit(1)

# Easy-install doesn't let us write files outside of the egg, so we'll have to
# just put them somewhere and try to install them later.
data_files = ['drivers/49-stellaris.rules', 'drivers/48-stm.rules']

with open('README') as readme_file:
        long_description = readme_file.read()

setup(
    name = 'owl-tools',
    description = 'Toolchain for the Owl Embedded Python Runtime System',
    version = VERSION,
    author = 'Thomas W. Barr',
    author_email = 'twb@embeddedpython.org',
    url = "http://embeddedpython.org/",

    license='MIT License',
    long_description=long_description,

    install_requires = ['pyserial'],

    classifiers=[
                 "Development Status :: 4 - Beta",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 2.7",
                 "Topic :: Software Development :: Embedded Systems"],

    package_dir={'owl_tools':''},
    packages=['owl_tools'],
    scripts=['mcu'],
    data_files=data_files,
)

