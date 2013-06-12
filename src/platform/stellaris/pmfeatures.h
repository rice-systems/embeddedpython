/* platform/pmfeatures.h
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.

 * IMPORTANT: All of the HAVE_* items in this file should also exist in the
 * PM_FEATURES dict in src/tools/pmImgCreator.py.  If the item is defined here,
 * the corresponding dict value should be True; False otherwise.
 */

#ifndef FEATURES_H_
#define FEATURES_H_


/** Defines the size of the static heap */
#if (defined PART_LM3S9B92) || (defined PART_LM3S9D92)
#define PM_HEAP_SIZE 0x14000
#endif
#ifdef PART_LM3S8962
#define PM_HEAP_SIZE 0xc000
#endif

// profiler
#define HAVE_PROFILER

#define STACK_PROTECTION

#define CORTEX_C_STACK_PROTECT

// streams
//#define HAVE_BRIDGES

//#define NUM_BRIDGES 2
//#define UART_BRIDGE 0
//#define GPIO_BRIDGE 1

/**
 * When defined, bytecodes PRINT_ITEM and PRINT_NEWLINE are supported. Along
 * with these, helper routines in the object type are compiled in that allow
 * printing of the object.
 * REQUIRES stdio.h to have snprintf()
 */
#define HAVE_PRINT

/**
 * When defined, the code to perform mark-sweep garbage collection is included
 * in the build and automatic GC is enabled.  When undefined the allocator
 * will distribute memory until none is left, after which a memory exception
 * will occur.
 */
#define HAVE_GC


/* #148 Create configurable float datatype */
/**
 * When defined, the code to support floating point objects is included
 * in the build.
 */
#define HAVE_FLOAT
#define PM_FLOAT_LITTLE_ENDIAN

/**
 * When defined, the code to support the keyword del is included in the build.
 * This involves the bytecodes: DELETE_SUBSCR, DELETE_NAME, DELETE_ATTR,
 * DELETE_GLOBAL and DELETE_FAST.
 */
#define HAVE_DEL

/**
 * When defined, the code to support the IMPORT_FROM and IMPORT_STAR styles
 * is included in the build.
 */
#define HAVE_IMPORTS

/* #157 Support default args */
/**
 * When defined, the code to support default arguments to functions is included
 * in the build.
 */
#define HAVE_DEFAULTARGS

/* Support var args */
/**
 * When defined, the code to support variable arguments to functions is included
 * in the build.
 */
#define HAVE_VARARGS

/* #160 Add support for string and tuple replication */
/**
 * When defined, the code to support sequence (list, tuple, string) replcation
 * is included in the build.
 * This feature is required by the builtin function __bi.map().
 */
#define HAVE_REPLICATION

/* #202 Implement classes in the vm */
/**
 * When defined, the code to support classes, instances, methods, etc.
 * is included in the build.
 */
#define HAVE_CLASSES

/**
 * When defined, enables autoboxing of set, list, dict and string types. This
 * allows operations of the form [].append(1). Requires HAVE_CLASSES.
 */
#define HAVE_AUTOBOX

/**
 * When defined, the code to support the assert statement is included
 * in the build.
 */
#define HAVE_ASSERT
#if defined(HAVE_ASSERT) && !defined(HAVE_CLASSES)
#error HAVE_ASSERT requires HAVE_CLASSES
#endif

/* #205 Add support for string format operation */
/**
 * When defined, the code to perform string formatting using the binary modulo
 * operator is included in the build.
 * REQUIRES stdio.h to have snprintf()
 */
#define HAVE_STRING_FORMAT

/* #256 Add support for closures */
/**
 * When defined, the code to support function closures is included in the 
 * build.
 */
#define HAVE_CLOSURES
#if defined(HAVE_CLOSURES) && !defined(HAVE_DEFAULTARGS)
#error HAVE_CLOSURES requires HAVE_DEFAULTARGS
#endif

/* adding support for simple slicing */
#define HAVE_SLICING

// foreign function interface
//#define HAVE_FFI

#endif /* FEATURES_H_ */
