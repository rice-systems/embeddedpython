/* platform/desktop/main.c
 *
 * This file is Copyright 2007, 2009 Dean Hall.
 * Copyright 2010 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#include "pm.h"


extern unsigned char usrlib_img[];


int main(void)
{
    PmReturn_t retval;

    retval = pm_init(usrlib_img);

    if (PM_RET_OK == retval)
    {
        retval = pm_run("main");
    }

    return (int) retval;
}
