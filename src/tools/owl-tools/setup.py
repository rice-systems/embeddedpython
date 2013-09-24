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

with open('README') as readme_file:
        long_description = readme_file.read()

setup(
    name = 'owl-tools',
    description = 'Toolchain for the Owl Embedded Python Runtime System',
    version = '0.2',
    author = 'Thomas W. Barr',
    author_email = 'twb@embeddedpython.org',

    license='LICENSE',
    long_description=long_description,

    package_dir={'owl_tools':''},
    packages=['owl_tools'],
    scripts=['mcu'],
)

