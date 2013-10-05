/* vm/plat.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __PLAT_H__
#define __PLAT_H__


/** 
 * \file
 * \brief PyMite's Porting Interface 
 */


/**
 * Initializes the platform as needed by the routines
 * in the platform implementation file.
 */
PmReturn_t plat_init(void);

/** De-initializes the platform after the VM is done running. */
PmReturn_t plat_deinit(void);

/**
 * Checks if there is an available byte.  Returns 0 if a call
 * to plat_getByte would have to wait or non-zero if plat_getByte
 * would return immediately if called.
 */
uint8_t plat_isDataAvail(void);

/**
 * Receives one byte from the default connection,
 * usually UART0 on a target device or stdio on the desktop
 */
PmReturn_t plat_getByte(uint8_t *b);


/**
 * Sends one byte out on the default connection,
 * usually UART0 on a target device or stdio on the desktop
 */
PmReturn_t plat_putByte(uint8_t b);


/**
 * Gets the number of timer ticks that have passed since system start.
 */
PmReturn_t plat_getMsTicks(uint32_t *r_ticks);


#ifdef HAVE_PROFILER
/**
 * sets profiler frequency
 */
PmReturn_t plat_setProfilerFrequency(int frequency);
#endif

#ifdef HAVE_FILESYSTEM_IMPORTS
PmReturn_t plat_fs_import(pPmString_t pname, uint8_t const **img);
#endif

#endif /* __PLAT_H__ */
