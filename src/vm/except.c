/* vm/except.c
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x20 

#include "pm.h"

void
except_fatal(char *msg)
{
    // at this point, the virtual machine is effectively dead.
    // we expect the heap to be corrupt and unusable. we can't report an error
    // because we may be in the middle of a garbage collect cycle, or something
    // equivalently horrible. we just try to report the error and spin forever.

    lib_printf("Fatal error: %s\n", msg);
    lib_printf("The virtual machine has stopped.\n");

    while (1) { };
}
    
