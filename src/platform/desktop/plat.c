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
void plat_printTrace(void);


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

void
plat_printTrace(void)
{
    /* Print traceback */
    pPmFrame_t pframe;
    pPmObj_t pstr;
    PmReturn_t retval;
    
    printf("\n");
    
    /* Get the top frame */
    pframe = FP;
    
    /* No way to print the native frame if that's where the exception
     * occurred (the fact that we were even in a native frame is
     * lost).
     */
    
    /* Print the remaining frame stack */
    for (;
	 pframe != C_NULL;
	 pframe = pframe->fo_back)
    {
	/* The last name in the names tuple of the code obj is the name */
	retval = tuple_getItem(co_getNames(pframe->fo_func->f_co),
                               -1, &pstr);
	if ((retval) != PM_RET_OK) break;
	
	printf("  ");
        obj_print((pPmObj_t) pstr, 0);
	printf("()\n");

    }
    printf("  <module>.\n");
}

/* void */
/* plat_reportError2(PmReturn_t result) */
/* { */
/*     /\* Print error *\/ */
/*     printf("Error:     0x%02X\n", result); */
/*     printf("  FileId:  0x%02X\n", gVmGlobal.errFileId); */
/*     printf("  LineNum: %d\n", gVmGlobal.errLineNum); */

/*     plat_printTrace(); */
/* } */

/*
 * Keys:
 *   0: error
 *   1: release
 *   2: vm file
 *   3: vm line
 *   4: py file
 *   5: py line
 */

void
plat_reportError(PmReturn_t result)
{

    // human readable error reporting
    /*lib_printf("---exception---\n");
    lib_printf("retval: %X\n", result);
    lib_printf("file id: %X\n", gVmGlobal.errFileId);
    lib_printf("line number: %d\n", gVmGlobal.errLineNum);

    if (gVmGlobal.pyErrFilename) {
        lib_printf("filename: ");
        string_print((pPmObj_t) gVmGlobal.pyErrFilename, 0);
        lib_printf("\n");
    }

    lib_printf("python line number: %d\n", gVmGlobal.pyErrLineNum);

    if (*gVmGlobal.errInfo) {
        lib_printf("info: ");
        lib_printf("%s", gVmGlobal.errInfo);
        lib_printf("\n");
    } 
    
    if (OBJ_GET_TYPE(gVmGlobal.errObj) != OBJ_TYPE_NON) {
        lib_printf("object: ");
        obj_print(gVmGlobal.errObj, 0);
        lib_printf("\n");
    }

    lib_printf("thread: %d\n", RUNNINGTHREAD->ptid->val);
    lib_printf("traceback:\n");
    plat_printTrace();
    lib_printf("-end exception-\n"); */

    // packed binary format
    plat_putByte(0x1d);

    lib_printf("0");
    plat_putByte(0x1f);
    lib_printf("%X", result);

    plat_putByte(0x1e);

    lib_printf("2");
    plat_putByte(0x1f);
    lib_printf("%X", gVmGlobal.errFileId);
    
    plat_putByte(0x1e);

    lib_printf("3");
    plat_putByte(0x1f);
    lib_printf("%d", gVmGlobal.errLineNum);

    if (gVmGlobal.pyErrFilename) {
        plat_putByte(0x1e);

        lib_printf("4");
        plat_putByte(0x1f);
        string_print((pPmObj_t) gVmGlobal.pyErrFilename, 0);
    }

    plat_putByte(0x1e);

    lib_printf("5");
    plat_putByte(0x1f);
    lib_printf("%d", gVmGlobal.pyErrLineNum);

    plat_putByte(0x1e);
    
    lib_printf("6");
    plat_putByte(0x1f);

    if (*gVmGlobal.errInfo) {
      lib_printf("%s", gVmGlobal.errInfo);
    } 
    
    if (OBJ_GET_TYPE(gVmGlobal.errObj) != OBJ_TYPE_NON) {
      obj_print(gVmGlobal.errObj, 0);
    }

    plat_putByte(0x1e);

    lib_printf("8");
    plat_putByte(0x1f);
    lib_printf("%d", RUNNINGTHREAD->ptid->val);

    plat_putByte(0x1e);

    lib_printf("7");

    plat_putByte(0x1f);
    plat_printTrace();
    
    plat_putByte(0x1d);

}

