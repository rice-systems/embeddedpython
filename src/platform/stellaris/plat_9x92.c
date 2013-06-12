/* platform/stellaris/plat_9x92.c
 *
 * Supports the TI Stellaris LM3S9x9x series parts.
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#undef __FILE_ID__
#define __FILE_ID__ 0x70


/** PyMite platform-specific routines for Stellaris Cortex-M3 target */

#if SUBMDL == LM3S9B92
#include "inc/lm3s9b92.h"
#elif SUBMDL == LM3S9D92
#include "inc/lm3s9d92.h"
#else
#error unsupported submdl in plat_9x92.c
#endif

#include "inc/hw_types.h"
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "inc/hw_sysctl.h"
#include "driverlib/interrupt.h"
#include "driverlib/systick.h"
#include "driverlib/gpio.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "usblib/usblib.h"
#include "usblib/usbcdc.h"
#include "usblib/device/usbdevice.h"
#include "usblib/device/usbdcdc.h"
#include "usb/plat_usb.h"
#include "pm.h"
#include "stellaris.h"

#define CALLBACK_MS 10
#define RESET_VAL 1000000000ul

unsigned int ticks = 0;

void ticker_callback(void);

bool usb_connected = false;

uint8_t pmHeapMem[PM_HEAP_SIZE] __attribute__ ((aligned (4)));

void
ticker_callback(void)
{
    PmReturn_t retval;

    ticks++;

    retval = pm_vmPeriodic(CALLBACK_MS * 1000);
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

    lib_printf("timed region: %d\n", time);
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
    
    // Enable the GPIO pin for the USB select and host power.
    MAP_GPIOPinTypeGPIOOutput(USBSEL_GPIO_PORT, USBSEL_GPIO_PIN);
    MAP_GPIOPinTypeGPIOOutput(USBPOW_GPIO_PORT, USBPOW_GPIO_PIN);

    // Wait for ports to be enabled.
    for(ulLoop = 0; ulLoop < 10; ulLoop++) {}

    // Power host power and enable device mode on switch
    MAP_GPIOPinWrite(USBSEL_GPIO_PORT, USBSEL_GPIO_PIN, USBSEL_GPIO_PIN);
    MAP_GPIOPinWrite(USBPOW_GPIO_PORT, USBPOW_GPIO_PIN, USBPOW_GPIO_PIN);

    // Set the clocking to run from the PLL at 50MHz
    MAP_SysCtlClockSet(SYSCTL_SYSDIV_4 | SYSCTL_USE_PLL | SYSCTL_OSC_MAIN |
                       SYSCTL_XTAL_16MHZ);

    // set up the timer /
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_32_BIT_OS);
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
    MAP_TimerConfigure(TIMER1_BASE, TIMER_CFG_32_BIT_PER);

    // the default load value isn't something sane.
    MAP_TimerLoadSet(TIMER1_BASE, TIMER_A, SysCtlClockGet());

    IntEnable(INT_TIMER1A);
    MAP_TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
    
    MAP_TimerEnable(TIMER1_BASE, TIMER_A);
#endif

    return PM_RET_OK;
}


PmReturn_t
plat_setProfilerFrequency(int frequency) {
#ifdef HAVE_PROFILER
    MAP_TimerLoadSet(TIMER1_BASE, TIMER_A, SysCtlClockGet() / frequency);
#endif

    return PM_RET_OK;
}

PmReturn_t
plat_init(void)
{
    // Set the systick timer and enable it.
    MAP_SysTickPeriodSet(MAP_SysCtlClockGet() / (1000 / CALLBACK_MS));
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
    tBoolean chars_avail;
    chars_avail = USBBufferDataAvailable(&g_usb_recv_buffer);

    return chars_avail ? 1 : 0;
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


static void
plat_printTrace(void)
{
    /* Print traceback */
    pPmFrame_t pframe;
    pPmObj_t pstr;
    PmReturn_t retval;
    
    lib_printf("\n");
    
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

        lib_printf("  ");
        obj_print(pstr, 0);
        lib_printf("()\n");
    }
    lib_printf("  <module>.\n");
}

#if 0
void
plat_reportError(PmReturn_t result)
{
    /* Print error */
    lib_printf("Error:     0x%02X\n", result);
    lib_printf("  FileId:  0x%02X\n", gVmGlobal.errFileId);
    lib_printf("  LineNum: %d\n", gVmGlobal.errLineNum);

    plat_printTrace();
}
#endif 

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
        if (OBJ_GET_TYPE((pPmObj_t) gVmGlobal.pyErrFilename) == OBJ_TYPE_STR) {
            string_print((pPmObj_t) gVmGlobal.pyErrFilename, 0);
        } else {
            lib_printf("(unknown)");
        }
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

