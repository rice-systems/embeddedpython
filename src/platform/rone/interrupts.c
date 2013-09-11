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

#include "inc/hw_memmap.h"

extern void ticker_callback(void);
extern void UARTIntHandler(void);

void __attribute__ ((interrupt)) sys_tick_handler (void) {
  ticker_callback();
}

void __attribute__ ((interrupt)) uart0_isr (void) {
  UARTIntHandler();
}

