# tools/build/autowrap/clean.py
#
# cleans names of functions and defines
#
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import os.path

OTHER_PREFIXES = ['tim']

class Cleaner:
    def __init__(self, fn):
        self.fn = os.path.basename(fn).split('.')[0]

    def clean(self, name):
        prefixes = [self.fn]

        # see if any of the alternate prefixes might apply in this file
        for prefix in OTHER_PREFIXES:
            if prefix in self.fn:
                prefixes.append(prefix)

        for prefix in prefixes:
            # ignore any capitalization when matching prefixes
            if name.lower().startswith(prefix.lower()):
                # strip off the prefix
                short = name[len(prefix):].strip('_')

                # we can only use the prefix if it's a valid python identifier
                if short[0].isalpha():
                    return short
                else:
                    return name
        
        return name
