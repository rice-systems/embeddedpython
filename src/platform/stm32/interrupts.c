// interrupts.c - Interrupt vectors for using GCC compilers

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

extern void stm32_usb_poll(void);
extern void ticker_callback(void);

void __attribute__ ((interrupt)) otg_fs_isr(void)
{
    stm32_usb_poll();
}

void __attribute__ ((interrupt)) hard_fault_handler(void)
{
    usbd_disconnect(1); 
    panic(1);
}

void __attribute__ ((interrupt)) mem_manage_handler(void)
{
    usbd_disconnect(1); 
    panic(2);
}   

void __attribute__ ((interrupt)) bus_fault_handler(void)
{
    usbd_disconnect(1); 
    panic(3);
}   

void __attribute__ ((interrupt)) usage_fault_handler(void)
{
    usbd_disconnect(1); 
    panic(4);
}   

void __attribute__ ((interrupt)) sys_tick_handler(void)
{
    ticker_callback();
}

void __attribute__ ((interrupt)) tim2_isr(void)
{
    plat_profiler_tick();
}


