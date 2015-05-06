// interrupts.c - Interrupt vectors for using CodeSourcery compilers

/* platform/interrupts.c
 *
 * The functions in this file are called directly by the hardware, then
 * dispatch into the VM. This file is here because different compilers have
 * different names for things. It should be used as the landing point for ALL
 * interrupts.
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#include "pm.h"
#include "tiva.h"
#include "interp.h"

#include "inc/hw_i2c.h" /* for I2C registers, e.g. IC */
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/usb.h"
#include "driverlib/i2c.h"
#include "driverlib/uart.h"
#include "driverlib/interrupt.h" /* for clearing interrupts */

#define __FILE_ID__ 0x23

extern void ticker_callback(void);

extern void USB0DeviceIntHandler(void);

// Snowflake moves the USB interrupt to what used to be the Ethernet interrupt.
#ifndef CLASS_IS_SNOWFLAKE
void __attribute__ ((interrupt)) usb0_isr (void);
#else
void __attribute__ ((interrupt)) eth_isr (void);
#endif

void __attribute__ ((naked)) hard_fault_handler (void);
void __attribute__ ((interrupt)) mem_manage_handler (void);
void __attribute__ ((interrupt)) bus_fault_handler (void);
void __attribute__ ((interrupt)) usage_fault_handler (void);
void __attribute__ ((interrupt)) sys_tick_handler (void);
void __attribute__ ((interrupt)) timer1a_isr (void);

/*********************************************
 * INTERRUPT HANDLERS
 *********************************************/
void __attribute__ ((interrupt)) hard_fault_handler (void) {
    USBDevDisconnect(USB0_BASE);
    panic(1);
}

void __attribute__ ((interrupt)) mem_manage_handler (void) {
    USBDevDisconnect(USB0_BASE);
    panic(2);
}

void __attribute__ ((interrupt)) bus_fault_handler (void) {
    USBDevDisconnect(USB0_BASE);
    panic(3);
}

void __attribute__ ((interrupt)) usage_fault_handler (void) {
    USBDevDisconnect(USB0_BASE);
    panic(4);
}

// Snowflake moves the USB interrupt to what used to be the Ethernet interrupt.
#if defined CLASS_IS_TM4C123 || defined CLASS_IS_TM4C129
void __attribute__ ((interrupt)) eth_isr (void) {
#else
void __attribute__ ((interrupt)) usb0_isr (void) {
#endif
    USB0DeviceIntHandler();
}

void __attribute__ ((interrupt)) sys_tick_handler (void) {
    ticker_callback();
}

void __attribute__ ((interrupt)) timer1a_isr (void) {
    plat_profiler_tick();
}


