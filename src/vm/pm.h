/* vm/pm.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __PM_H__
#define __PM_H__


/**
 * \file
 * \brief PyMite Header
 *
 * Include things that are needed by nearly everything.
 */


#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>


/** null for C code */
#define C_NULL 0

/** false for C code */
#define C_FALSE 0

/** true for C code */
#define C_TRUE (!C_FALSE)

/** Comparison result is that items are equal */
#define C_EQ (int8_t)0

/** Comparison result is that items are not equal */
#define C_NEQ (int8_t)-1

/** Comparison result is that item1 is less than item2 */
#define C_LT (int8_t)-1

/** Comparison result is that item1 is greater than item2 */
#define C_GT (int8_t)1

/** Items cannot be compared */
#define C_CMP_ERR (int8_t)-10

/** PORT inline for C code */
#define INLINE __inline__


/**
 * Returns an exception error code and stores debug data
 *
 * This macro must be used as an rval statement.  That is, it must
 * be used after an assignment such as "retval = " or a return statement
 */
#if __DEBUG__
#define PM_RAISE(retexn, exn) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errFileId = __FILE_ID__; \
            gVmGlobal.errLineNum = (uint16_t)__LINE__; \
            gVmGlobal.errObj = PM_NONE; \
            gVmGlobal.errInfo = ""; \
        } while (0)
#else
#define PM_RAISE(retexn, exn) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errObj = PM_NONE; \
            gVmGlobal.errInfo = ""; \
        } while (0)
#endif

#if __DEBUG__
#define PM_RERAISE(retexn, exn) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errFileId = __FILE_ID__; \
            gVmGlobal.errLineNum = (uint16_t)__LINE__; \
        } while (0)
#else
#define PM_RERAISE(retexn, exn) \
        do \
        { \
            retexn = (exn); \
        } while (0)
#endif

#if __DEBUG__
#define PM_RAISE_WITH_OBJ(retexn, exn, obj) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errFileId = __FILE_ID__; \
            gVmGlobal.errLineNum = (uint16_t)__LINE__; \
            gVmGlobal.errObj = obj; \
            gVmGlobal.errInfo = ""; \
        } while (0)
#else
#define PM_RAISE_WITH_OBJ(retexn, exn, obj) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errObj = obj; \
            gVmGlobal.errInfo = ""; \
        } while (0)
#endif

#if __DEBUG__
#define PM_RAISE_WITH_INFO(retexn, exn, info) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errFileId = __FILE_ID__; \
            gVmGlobal.errLineNum = (uint16_t)__LINE__; \
            gVmGlobal.errObj = PM_NONE; \
            gVmGlobal.errInfo = info; \
        } while (0)
#else
#define PM_RAISE_WITH_INFO(retexn, exn, info) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errObj = PM_NONE; \
            gVmGlobal.errInfo = info; \
        } while (0)
#endif
        
#if __DEBUG__
#define PM_RAISE_WITH_INFO_AND_OBJ(retexn, exn, info, obj) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errFileId = __FILE_ID__; \
            gVmGlobal.errLineNum = (uint16_t)__LINE__; \
            gVmGlobal.errObj = obj; \
            gVmGlobal.errInfo = info; \
        } while (0)
#else
#define PM_RAISE_WITH_INFO_AND_OBJ(retexn, exn, info, obj) \
        do \
        { \
            retexn = (exn); \
            gVmGlobal.errObj = obj; \
            gVmGlobal.errInfo = info; \
        } while (0)
#endif

/** if retval is not OK, break from the block */
#define PM_BREAK_IF_ERROR(retval) if((retval) != PM_RET_OK)break

/** return an error code if it is not PM_RET_OK */
#define PM_RETURN_IF_ERROR(retval)  if((retval) != PM_RET_OK) \
                                        return (retval)

/** return an error code if it is not PM_RET_OK and set liveObj to Null */
#define PM_RETURN_IF_ERROR_SET_NULL(retval) \
    do \
    { \
         if((retval) != PM_RET_OK) \
         { \
             FP->liveObj = C_NULL; \
             return retval; \
         } \
    } \
    while (0)

/** print an error message if argument is not PM_RET_OK */
#define PM_REPORT_IF_ERROR(retval)   if ((retval) != PM_RET_OK) \
                                        except_reportError(retval)

#if __DEBUG__
/** If the boolean expression fails, return the ASSERT error code */
#define C_ASSERT(boolexpr) \
    do \
    { \
        if (!((boolexpr))) \
        { \
            gVmGlobal.errFileId = __FILE_ID__; \
            gVmGlobal.errLineNum = (uint16_t)__LINE__; \
            except_reportError(PM_RET_ASSERT_FAIL); \
            return PM_RET_ASSERT_FAIL; \
        } \
    } \
    while (0)

#else
/** Assert statements are removed from production code */
#define C_ASSERT(boolexpr)
#endif

/** Use as the first argument to C_DEBUG_PRINT for low volume messages */
#define VERBOSITY_LOW 1

/** Use as the first argument to C_DEBUG_PRINT for medium volume messages */
#define VERBOSITY_MEDIUM 2

/** Use as the first argument to C_DEBUG_PRINT for high volume messages */
#define VERBOSITY_HIGH 3

#if __DEBUG__

/** To be used to set DEBUG_PRINT_VERBOSITY to a value so no prints occur */
#define VERBOSITY_OFF 0

/** Sets the level of verbosity to allow in debug prints */
#define DEBUG_PRINT_VERBOSITY VERBOSITY_OFF

/** Prints a debug message when the verbosity is within the set value */
#define C_DEBUG_PRINT(v, f, ...) \
    do \
    { \
        if (DEBUG_PRINT_VERBOSITY >= (v)) \
        { \
            lib_printf("PM_DEBUG: " f, ## __VA_ARGS__); \
        } \
    } \
    while (0)

#else
#define C_DEBUG_PRINT(...)
#endif


/**
 * Return values for system functions
 * to report status, errors, exceptions, etc.
 * Normally, functions which use these values
 * should propagate the same return value
 * up the call tree to the interpreter.
 */
typedef enum PmReturn_e
{
    /* general status return values */
    PM_RET_OK = 0,              /**< Everything is ok */
    PM_RET_NO = 0xFF,           /**< General "no result" */
    PM_RET_ERR = 0xFE,          /**< General failure */
    PM_RET_STUB = 0xFD,         /**< Return val for stub fxn */
    PM_RET_ASSERT_FAIL = 0xFC,  /**< Assertion failure */
    PM_RET_FRAME_SWITCH = 0xFB, /**< Frame pointer was modified */

    /* return vals that indicate an exception occured */
    PM_RET_EX = 0xE0,           /**< General exception */
    PM_RET_EX_EXIT = 0xE1,      /**< System exit */
    PM_RET_EX_IO = 0xE2,        /**< Input/output error */
    PM_RET_EX_ZDIV = 0xE3,      /**< Zero division error */
    PM_RET_EX_ASSRT = 0xE4,     /**< Assertion error */
    PM_RET_EX_ATTR = 0xE5,      /**< Attribute error */
    PM_RET_EX_IMPRT = 0xE6,     /**< Import error */
    PM_RET_EX_INDX = 0xE7,      /**< Index error */
    PM_RET_EX_KEY = 0xE8,       /**< Key error */
    PM_RET_EX_MEM = 0xE9,       /**< Memory error */
    PM_RET_EX_NAME = 0xEA,      /**< Name error */
    PM_RET_EX_SYNTAX = 0xEB,    /**< Syntax error */
    PM_RET_EX_SYS = 0xEC,       /**< System error */
    PM_RET_EX_TYPE = 0xED,      /**< Type error */
    PM_RET_EX_VAL = 0xEE,       /**< Value error */
    PM_RET_EX_STOP = 0xEF,      /**< Stop iteration */
    PM_RET_EX_WARN = 0xF0,      /**< Warning */
    PM_RET_EX_USER = 0xF1,      /**< User error */
    PM_RET_EX_UNBOUND = 0xF2,   /**< Unbound local error */
} PmReturn_t;


extern volatile uint32_t pm_timerMsTicks;


/* WARNING: The order of the following includes is critical */
#include "obj.h"
#include "seq.h"
#include "xrange.h"
#include "tuple.h"
#include "seglist.h"
#include "list.h"
#include "strobj.h"
#include "heap.h"
#include "int.h"
#include "dict.h"
#include "codeobj.h"
#include "func.h"
#include "module.h"
#include "frame.h"
#include "interp.h"
#include "img.h"
#include "profiler.h"
#include "thread.h"


#include "set.h"
#include "global.h"
#include "class.h"
#include "float.h"

#include "packtuple.h"

#include "plat.h"
#include "foreign.h"
#include "except.h"

/* included for lib_printf */
#include <stdarg.h>
#include <string.h>

/**
 * Initializes the PyMite virtual machine and indexes the user's application
 * image.  The VM heap and globals are reset.  The argument, pusrimg, may be
 * null for interactive sessions.
 *
 * @param pusrimg       Address of the user image in the memory space
 * @return Return status
 */
PmReturn_t pm_init(uint8_t *pusrimg);

/**
 * Executes the named module
 *
 * @param modstr        Name of module to run
 * @return Return status
 */
PmReturn_t pm_run(char const *modstr);

/**
 * Needs to be called periodically by the host program.
 * For the desktop target, it is periodically called using a signal.
 * For embedded targets, it needs to be called periodically. It should
 * be called from a timer interrupt.
 *
 * @param usecsSinceLastCall Microseconds (not less than those) that passed
 *                           since last call. This must be <64535.
 * @return Return status
 */
PmReturn_t pm_vmPeriodic(uint16_t usecsSinceLastCall);


/* lib_ functions */
int32_t lib_printf(const char *pcString, ...) 
    __attribute__ ((format (printf, 1, 2)));
int32_t lib_snprintf(char *pstr, size_t size, const char *pformat, ...)
    __attribute__ ((format (printf, 3, 4)));

#endif /* __PM_H__ */


#ifdef __cplusplus
}
#endif

