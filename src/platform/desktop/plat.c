/* platform/desktop/plat.c
 *
 * This file is Copyright 2006, 2007, 2009 Dean Hall.
 * Copyright 2010 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x70


/** PyMite platform-specific routines for Desktop target */


#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <stdlib.h>

#include "pm.h"

#define MAX_FILENAME_SIZE 20

void plat_sigalrm_handler(int signal);

uint8_t pmHeapMem[PM_HEAP_SIZE];

#ifdef HAVE_FILESYSTEM_IMPORTS
PmReturn_t
plat_fs_import(pPmString_t pname, uint8_t const **img)
{
    uint8_t fname[MAX_FILENAME_SIZE];

    int stat_res, img_size, fd;
    struct stat img_stat;
    PmReturn_t retval = PM_RET_OK;

    // construct the file name to load
    if ((pname->length) + 5 > MAX_FILENAME_SIZE) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_IMPRT, "file name too long");
        return retval;
    }

    memcpy(fname, pname->val, pname->length);
    fname[pname->length] = '.';
    fname[pname->length+1] = 'p';
    fname[pname->length+2] = 'm';
    fname[pname->length+3] = 'c';
    fname[pname->length+4] = '\0';

    // see if we can actually open it
    stat_res = stat((const char *) fname, &img_stat);
    
    if (stat_res != 0) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_IMPRT, "image not found");
        return retval;
    }

    img_size = (int) img_stat.st_size;

    // open it
    fd = open((const char *)fname, O_RDONLY);

    if (fd < 0) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_IMPRT, "couldn't open image");
        return retval;
    }

    // map it
    *img = mmap(NULL, img_size, PROT_READ, MAP_PRIVATE, fd, 0);

    if (*img == NULL) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_IMPRT, "couldn't map image");
        return retval;
    }

    return retval;
}
#endif

#ifdef HAVE_PROFILER
// not really much we can do here...
PmReturn_t
plat_setProfilerFrequency(int frequency) {

    return PM_RET_OK;
}
#endif

static int c = -2;

/* Desktop target shall use stdio for I/O routines. */
PmReturn_t
plat_init(void)
{
    int flags;

    /* Make stdin non-blocking */
    flags = fcntl(0, F_GETFL, 0); /* get current file status flags */
    flags |= O_NONBLOCK;	  /* turn off blocking flag */
    fcntl(0, F_SETFL, flags);     /* set up non-blocking reads */

    /* Let POSIX' SIGALRM fire every full millisecond. 
     *
     * #67 Using sigaction complicates the use of getchar (below),
     * so signal() is used instead.
     */
    signal(SIGALRM, plat_sigalrm_handler);
    ualarm(1000, 1000);

    return PM_RET_OK;
}


/* Disables the peripherals and interrupts */
PmReturn_t
plat_deinit(void)
{
    /* Cancel alarm and set the alarm handler to the default */
    ualarm(0, 0);
    signal(SIGALRM, SIG_DFL);

    return PM_RET_OK;
}


void
plat_sigalrm_handler(int signal)
{
    PmReturn_t retval;

#ifdef HAVE_PROFILER
    profiler_tick();
#endif

    retval = pm_vmPeriodic(1000);
    PM_REPORT_IF_ERROR(retval);
}


/* Desktop target shall use stdio for I/O routines */
uint8_t
plat_isDataAvail()
{
    if (c != -2)
    {
        /* Character already available (repeat call) */
        return 1;
    }

    c = getchar();
    if ((c == EOF) && (errno == EAGAIN))
    {
        /* No data available */
        c = -2;
        return 0;
    }

    /* Data available and has been read */
    return 1;
}

/* Desktop target shall use stdio for I/O routines */
PmReturn_t
plat_getByte(uint8_t *b)
{
    PmReturn_t retval = PM_RET_OK;

    if (c == -2) 
    {
        /* Data not read in isDataAvail, "block" */
        c = getchar();
        while ((c == EOF) && (errno == EAGAIN))
        {
            c = getchar();
        }
    }

    *b = c & 0xFF;

    if (c == EOF)
    {
        PM_RAISE(retval, PM_RET_EX_IO);
    }

    /* Data has been read */
    c = -2;

    return retval;
}


/* Desktop target shall use stdio for I/O routines */
PmReturn_t
plat_putByte(uint8_t b)
{
    int i;
    PmReturn_t retval = PM_RET_OK;

    i = putchar(b);
    fflush(stdout);

    if ((i != b) || (i == EOF))
    {
        PM_RAISE(retval, PM_RET_EX_IO);
    }

    return retval;
}


PmReturn_t
plat_getMsTicks(uint32_t *r_ticks)
{
    *r_ticks = pm_timerMsTicks;

    return PM_RET_OK;
}

