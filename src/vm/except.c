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

// define this to bypass the normal exception reporting mechanism.
// #define HUMAN_READABLE_ERRRORS

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

pPmFrame_t
except_getFrameAtDepth(uint16_t depth)
{
    pPmFrame_t pframe;

    // start at the most recent call
    pframe = FP;

    while(depth--)
    {
        // walk back
        pframe = pframe->fo_back;

        // bail if we hit the bottom of the stack.
        if (pframe == C_NULL)
        {
            return pframe;
        }
    }

    return pframe;
}

uint16_t
except_getStackDepth(void)
{
    pPmFrame_t pframe;
    uint16_t depth = 1;

    // start at the most recent call
    pframe = FP;

    while(1)
    {
        // walk back
        pframe = pframe->fo_back;

        // stop when we hit the bottom of the stack.
        if (pframe == C_NULL)
        {
            return depth;
        }

        depth++;
    }
}

void
except_printTrace(void)
{
    /* Print traceback */
    pPmFrame_t pframe;
    pPmObj_t pmodname;
    pPmString_t perrfilename;
    PmReturn_t retval;
    uint16_t line, depth;
    
    lib_printf("\n");

    depth = except_getStackDepth();
    
    /* No way to print the native frame if that's where the exception
     * occurred (the fact that we were even in a native frame is
     * lost).
     */

    /* make sure we're actually running a program */
    if (RUNNINGTHREAD == C_NULL)
    {
        lib_printf("  (not running a thread)\n");
    }
    else
    {
        /* Print the remaining frame stack */
        while (depth--)
        {
            pframe = except_getFrameAtDepth(depth);

            /* The last name in the names tuple of the code obj is the function name */
            retval = tuple_getItem(co_getNames(pframe->fo_func->f_co),
                                       -1, &pmodname);

            if ((retval) != PM_RET_OK)
                break;

            /* get the line number */
            line = co_getLineno(pframe->fo_func->f_co, pframe->fo_ip);

            /* and the file name */
            perrfilename = co_getFilename(pframe->fo_func->f_co);
            
            lib_printf("  File \"");
            obj_print((pPmObj_t) perrfilename, 0);
            lib_printf("\", line %d, in ", line);
            obj_print((pPmObj_t) pmodname, 0);
            lib_printf("\n");

        }
    }
}

void
except_reportError(PmReturn_t result)
{
#ifdef HUMAN_READABLE_ERRRORS
    lib_printf("---exception---\n");
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
    lib_printf("-end exception-\n");
#else // HUMAN_READABLE_ERRRORS
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
    except_printTrace();
    
    plat_putByte(0x1d);
#endif // HUMAN_READABLE_ERRRORS
}
