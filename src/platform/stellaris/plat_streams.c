/* platform/stellaris/plat_streams.c
 *
 * Stream ISR handlers.
 *
 * Copyright 2012 Rice University.
 *
 * This file is a proprietary and confidential part of the Owl Embedded Python
 * System. It is not to be distributed without the express permission of its
 * authors.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x70

#include "inc/lm3s9b92.h"
#include "inc/hw_types.h"
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "driverlib/interrupt.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/uart.h"
#include "driverlib/timer.h"

#include "pm.h"

void
UART0IntHandler(void)
{
    unsigned long ulStatus;
    uint8_t latest_byte;
    PmReturn_t retval;

    ulStatus = MAP_UARTIntStatus(UART0_BASE, true);
    MAP_UARTIntClear(UART0_BASE, ulStatus);
    
    /* if we have a place to put it, put characters in the buffer */
    while(ROM_UARTCharsAvail(UART0_BASE))
    {

        latest_byte = ROM_UARTCharGetNonBlocking(UART0_BASE);
        retval = bridge_produce(UART_BRIDGE, &latest_byte, 1);

        if (retval != PM_RET_OK)
        {
            // not a whole lot we can do about it...
            break;
        }
    }
}

#define ALL_PINS 0xff
//#define TIME_ISR

void
GPIOIntHandler(unsigned long port)
{
    uint8_t values;
    uint8_t message[2 * sizeof(unsigned long) + 1];
    void *time = &pm_timerMsTicks;

#ifdef TIME_ISR
    plat_timer_start();
#endif

    /* clear all the interrupts for this port */
    GPIOPinIntClear(port, ALL_PINS);
    
    /* read the value of the port */
    values = GPIOPinRead(port, ALL_PINS);

    /* pack the data into a nine byte message */
    memcpy(message, &port, sizeof(unsigned long));
    message[sizeof(unsigned long)] = values;
    memcpy(&message[sizeof(unsigned long)+1], time, sizeof(unsigned long));

#ifdef TIME_ISR
    plat_timer_stop();
#endif

    /* send it to the subscribers */
    bridge_produce(GPIO_BRIDGE, message, 9);
}

