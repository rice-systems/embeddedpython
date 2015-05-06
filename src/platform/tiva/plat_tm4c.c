/* platform/tiva/plat_tm4c.c
 *
 * Supports the TI Tiva C series parts.
 *
 * Copyright 2014 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x70


/** Platform-specific routines for Tiva Cortex-M4 target */

#include "pm.h"
#include "tiva.h"

#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "inc/hw_sysctl.h"
#include "inc/hw_gpio.h"
#include "driverlib/i2c.h"
#include "driverlib/interrupt.h"
#include "driverlib/systick.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/uart.h"
#include "usblib/usblib.h"
#include "usblib/usbcdc.h"
#include "usblib/device/usbdevice.h"
#include "usblib/device/usbdcdc.h"
#include "usb/plat_usb.h"


#define TICKS_PER_SECOND 100
#define RESET_VAL 1000000000ul

unsigned int ticks = 0;

void ticker_callback(void);
unsigned long plat_timer_stop_and_read(void);

bool usb_connected = false;

uint8_t pmHeapMem[PM_HEAP_SIZE] __attribute__ ((aligned (4)));

static uint32_t ui32SysClock;


void
ticker_callback(void)
{
    PmReturn_t retval;

    ticks++;

    /* 
     * pm_vmPeriodic takes microseconds:
     * 1000000us/second * second/tick
     */
    retval = pm_vmPeriodic(1000000 / TICKS_PER_SECOND);
    PM_REPORT_IF_ERROR(retval);
}


void
plat_timer_start(void)
{
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, RESET_VAL);
    MAP_TimerEnable(TIMER0_BASE, TIMER_A);
}


void
plat_timer_stop(void)
{
    unsigned long time;

    time = RESET_VAL - MAP_TimerValueGet(TIMER0_BASE, TIMER_A);
    MAP_TimerDisable(TIMER0_BASE, TIMER_A);
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, RESET_VAL);

    lib_printf("timed region: %d\n", (int)time);
}

unsigned long
plat_timer_stop_and_read(void)
{
    unsigned long time;

    time = RESET_VAL - MAP_TimerValueGet(TIMER0_BASE, TIMER_A);
    MAP_TimerDisable(TIMER0_BASE, TIMER_A);
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, RESET_VAL);

    return time;
}

#ifdef HAVE_PROFILER
void
plat_profiler_tick(void)
{
    MAP_TimerIntClear(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
    profiler_tick();
}
#else
void
plat_profiler_tick(void)
{
    panic(10); // shouldn't happen
}
#endif

PmReturn_t
plat_preinit(void)
{
    volatile unsigned long ulLoop;

    FPUEnable();
    FPUStackingEnable();
    
    /* If we don't run the Snowflake part fast enough, USB never wakes up */
#if defined PART_TM4C129XNCZAD || defined PART_TM4C1294NCPDT
    // Run from the PLL at 120 MHz.
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_480), 120000000);
#else
    // Set the clocking to run from the PLL at 50MHz
    MAP_SysCtlClockSet(SYSCTL_SYSDIV_4 | SYSCTL_USE_PLL |
                                      SYSCTL_OSC_MAIN | SYSCTL_XTAL_16MHZ);
#endif
    
    // Enable the GPIO ports.
    MAP_SysCtlPeripheralEnable(LED_SYSCTL_PORT);
    MAP_SysCtlPeripheralEnable(SWITCH_SYSCTL_PORT);
    MAP_SysCtlPeripheralEnable(USBSEL_SYSCTL_PORT);
    MAP_SysCtlPeripheralEnable(USBPOW_SYSCTL_PORT);

    // Wait for ports to be enabled.
    for(ulLoop = 0; ulLoop < 10; ulLoop++) {}

    // Enable the GPIO pin for the pushbutton as a digital input.
    MAP_GPIOPinTypeGPIOInput(SWITCH_GPIO_PORT, SWITCH_GPIO_PIN);
    MAP_GPIOPadConfigSet(SWITCH_GPIO_PORT, SWITCH_GPIO_PIN, GPIO_STRENGTH_2MA,
                         GPIO_PIN_TYPE_STD_WPU);

    // Enable the GPIO pin for the LED as a digital output.
    MAP_GPIOPinTypeGPIOOutput(LED_GPIO_PORT, LED_GPIO_PIN);

    // The LM4F GPIO pins need to be properly set up for USB depending on part
#ifdef PART_TM4C123GH6PGE
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);
    GPIOPinConfigure(GPIO_PG4_USB0EPEN);
    GPIOPinTypeUSBDigital(GPIO_PORTG_BASE, GPIO_PIN_4);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);
    GPIOPinTypeUSBAnalog(GPIO_PORTL_BASE, GPIO_PIN_6 | GPIO_PIN_7);
    GPIOPinTypeUSBAnalog(GPIO_PORTB_BASE, GPIO_PIN_0 | GPIO_PIN_1);
#endif

#if defined PART_TM4C129XNCZAD || defined PART_TM4C1294NCPDT
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);

    /* Unlock the GPIO so we can switch the mode properly */
    HWREG(GPIO_PORTD_BASE + GPIO_O_LOCK) = GPIO_LOCK_KEY;
    HWREG(GPIO_PORTD_BASE + GPIO_O_CR) = 0xff;
    MAP_GPIOPinConfigure(GPIO_PD6_USB0EPEN);
    MAP_GPIOPinConfigure(GPIO_PD7_USB0PFLT);
    MAP_GPIOPinTypeUSBAnalog(GPIO_PORTB_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    MAP_GPIOPinTypeUSBDigital(GPIO_PORTD_BASE, GPIO_PIN_6 | GPIO_PIN_7);
    MAP_GPIOPinTypeUSBAnalog(GPIO_PORTL_BASE, GPIO_PIN_6 | GPIO_PIN_7);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_USB0);
    USBStackModeSet(0, eUSBModeDevice, 0);
#endif

#ifdef TIVAWARE
    // Erratum workaround for silicon revision A1.  VBUS must have pull-down.
    if(CLASS_IS_BLIZZARD && REVISION_IS_A1)
    {
        HWREG(GPIO_PORTB_BASE + GPIO_O_PDR) |= GPIO_PIN_1;
    }
#endif

    // set up the timer /
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

#ifdef TIVAWARE
    // for TivaWare
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_ONE_SHOT);
#else
    // for legacy Stellarisware
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_32_BIT_OS);
#endif

    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, RESET_VAL);
    MAP_TimerIntDisable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Initialize the transmit and receive buffers.
    USBBufferInit(&g_usb_recv_buffer);
    USBBufferInit(&g_usb_xmit_buffer);

    // Pass the device information to the USB library and place the device
    // on the bus.
    if (USBDCDCInit(0, &g_sCDCDevice) == NULL)
    {
        panic(8);
    }

    MAP_IntMasterEnable();
    
#ifdef HAVE_PROFILER
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    
#ifdef TIVAWARE
    // for TivaWare
    MAP_TimerConfigure(TIMER1_BASE, TIMER_CFG_ONE_SHOT);
#else
    // for legacy Stellarisware
    MAP_TimerConfigure(TIMER1_BASE, TIMER_CFG_32_BIT_PER);
#endif

    // the default load value isn't something sane.
    MAP_TimerLoadSet(TIMER1_BASE, TIMER_A, ui32SysClock);

    IntEnable(INT_TIMER1A);
    MAP_TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
    
    MAP_TimerEnable(TIMER1_BASE, TIMER_A);
#endif

    return PM_RET_OK;
}


PmReturn_t
plat_setProfilerFrequency(int frequency) {
#ifdef HAVE_PROFILER
    MAP_TimerLoadSet(TIMER1_BASE, TIMER_A, ui32SysClock / frequency);
#endif

    return PM_RET_OK;
}

PmReturn_t
plat_init(void)
{
    // Set the systick timer and enable it.
    MAP_SysTickPeriodSet(ui32SysClock / TICKS_PER_SECOND);
    MAP_SysTickIntEnable();
    MAP_SysTickEnable();

    return PM_RET_OK;
}


PmReturn_t
plat_deinit(void)
{
    // Is anything needed?
    return PM_RET_OK;
}


void plat_cts(int value)
{

}


PmReturn_t
plat_getByte(uint8_t *b)
{
    unsigned long ulRead;
    PmReturn_t retval = PM_RET_OK;

    // Wait for data in the buffer
    while(!plat_isDataAvail()) ;

    // Read byte
    ulRead = USBBufferRead(&g_usb_recv_buffer, b, 1);

    if (!ulRead)
    {
        PM_RAISE(retval, PM_RET_EX_IO);
    }    
    
    return retval;
}


uint8_t
plat_isDataAvail(void)
{
    // avoid doing this driver call with an explicit temp variable becuase its
    // return type changes from StellarisWare to TivaWare

    return USBBufferDataAvailable(&g_usb_recv_buffer) ? 1 : 0;
}  


PmReturn_t
plat_putByte(uint8_t b)
{
    if (usb_connected) {
        // Wait for space in the buffer
        while (!USBBufferSpaceAvailable(&g_usb_xmit_buffer)) ;

        // Write byte
        USBBufferWrite(&g_usb_xmit_buffer, &b, 1);
    }

    return PM_RET_OK;
}


PmReturn_t
plat_getMsTicks(uint32_t *r_ticks)
{
    // returns count from calls to pm_vmPeriodic()
    *r_ticks = pm_timerMsTicks;

    return PM_RET_OK;
}

