/* platform/stellaris/plat_8962.c
 *
 * Supports the TI Stellaris LM3S8962 series parts.
 *
 * Copyright 2013 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#undef __FILE_ID__
#define __FILE_ID__ 0x70


/** PyMite platform-specific routines for Stellaris Cortex-M3 target */

#include "inc/lm3s8962.h"
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
#include "driverlib/uart.h"
#include "pm.h"
#include "plat.h"
#include "stellaris.h"

#define CALLBACK_MS 1
#define RESET_VAL 1000000000ul

tBoolean no_usb = false;
unsigned int ticks = 0;

uint8_t pmHeapMem[PM_HEAP_SIZE] __attribute__ ((aligned (4)));

void ticker_callback(void);
void UARTIntHandler(void);

void
ticker_callback(void)
{
    PmReturn_t retval;

    ticks++;

    retval = pm_vmPeriodic(CALLBACK_MS * 1000);
    PM_REPORT_IF_ERROR(retval);
}


PmReturn_t
plat_setProfilerFrequency(int frequency) {
#ifdef HAVE_PROFILER
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, SysCtlClockGet() / frequency);
#endif

    return PM_RET_OK;
}

#ifdef HAVE_PROFILER
void
plat_profiler_tick(void)
{
    MAP_TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    profiler_tick();
}
#else
void
plat_profiler_tick(void)
{
    panic(10); // shouldn't happen
}
#endif

void
plat_heartbeat(int setting) {
    if (setting) {
        MAP_GPIOPinWrite(LED_GPIO_PORT, LED_GPIO_PIN, 0x00);
    } else {
        MAP_GPIOPinWrite(LED_GPIO_PORT, LED_GPIO_PIN, LED_GPIO_PIN);
    }
}


PmReturn_t
plat_preinit(void)
{
    volatile unsigned long ulLoop;

    // If running on Rev A2 silicon, turn the LDO voltage up to 2.75V.  This is
    // a workaround to allow the PLL to operate reliably.
    if(REVISION_IS_A2)
    {
        MAP_SysCtlLDOSet(SYSCTL_LDO_2_75V);
    }


    // Set the clocking to run at 50MHz from the PLL.
    MAP_SysCtlClockSet(SYSCTL_SYSDIV_4 | SYSCTL_USE_PLL | SYSCTL_OSC_MAIN |
                       SYSCTL_XTAL_8MHZ);
    MAP_SysCtlPWMClockSet(SYSCTL_PWMDIV_1);

    // Enable the GPIO pin for the pushbutton as a digital input.
    MAP_SysCtlPeripheralEnable(SWITCH_SYSCTL_PORT);
    MAP_GPIOPinTypeGPIOInput(SWITCH_GPIO_PORT, SWITCH_GPIO_PIN);
    MAP_GPIOPadConfigSet(SWITCH_GPIO_PORT, SWITCH_GPIO_PIN, GPIO_STRENGTH_2MA,
                         GPIO_PIN_TYPE_STD_WPU);

    // Enable the GPIO pin for the LED as a digital output.
    MAP_SysCtlPeripheralEnable(LED_SYSCTL_PORT);
    MAP_GPIOPinTypeGPIOOutput(LED_GPIO_PORT, LED_GPIO_PIN);

    // check to see if we're connected to USB
    MAP_SysCtlPeripheralEnable(USBSENSE_SYSCTL_PORT);
    for(ulLoop = 0; ulLoop < 10; ulLoop++) {}
    
    MAP_GPIOPinTypeGPIOInput(USBSENSE_GPIO_PORT, USBSENSE_GPIO_PIN);
    MAP_GPIOPadConfigSet(USBSENSE_GPIO_PORT, USBSENSE_GPIO_PIN, GPIO_STRENGTH_2MA,
                         GPIO_PIN_TYPE_STD_WPD);
    for(ulLoop = 0; ulLoop < 10; ulLoop++) {}

    if (MAP_GPIOPinRead(USBSENSE_GPIO_PORT, USBSENSE_GPIO_PIN)) {
      no_usb = false;
    } else {
      no_usb = true;
    }

    // enable the flow control pin
    if (!no_usb) {
      MAP_SysCtlPeripheralEnable(CTS_SYSCTL_PORT);
      for(ulLoop = 0; ulLoop < 10; ulLoop++) {}
      MAP_GPIOPinTypeGPIOOutput(CTS_GPIO_PORT, CTS_GPIO_PIN);
      plat_cts(1); // CTS is active LOW!
    }

    //init the rone hardware
    // rone_preinit();
    MAP_IntMasterEnable();

    if (!no_usb) {
      // Set up UART pins
      MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
      MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);

      // Wait for ports to be enabled.
      for(ulLoop = 0; ulLoop < 10; ulLoop++) {}

      MAP_GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

      // Initialize UART 
      MAP_UARTConfigSetExpClk(UART0_BASE, MAP_SysCtlClockGet(), 230400,
                              (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE |
                               UART_CONFIG_PAR_NONE));

      // flush the UART buffer
      while (UARTCharsAvail(UART0_BASE)) {
          UARTCharGet(UART0_BASE);
      }

      UARTRxErrorClear(UART0_BASE);

      // Initialize UART interrupt
      IntEnable(INT_UART0);
      MAP_UARTIntEnable(UART0_BASE, UART_INT_RX);
      MAP_UARTFIFOLevelSet(UART0_BASE, UART_FIFO_TX4_8, UART_FIFO_RX4_8);
    }

    // Set the systick timer and enable it.
    MAP_SysTickPeriodSet(MAP_SysCtlClockGet() / (1000 / CALLBACK_MS));
    MAP_SysTickIntEnable();
    MAP_SysTickEnable();

    return PM_RET_OK;
}


PmReturn_t
plat_init(void)
{
    // rone_init();

    return PM_RET_OK;
}


PmReturn_t
plat_deinit(void)
{
    return PM_RET_OK;
}


void plat_cts(int value)
{
    if (!no_usb) {
      MAP_GPIOPinWrite(CTS_GPIO_PORT, CTS_GPIO_PIN, value ? CTS_GPIO_PIN : 0);
    }
}


void UARTIntHandler(void)
{
    unsigned long error;
    
    plat_cts(1);
    UARTIntClear(UART0_BASE, UART_INT_RX);
    error = UARTRxErrorGet(UART0_BASE);
    
    if (error) {
        panic(4);
    }
}


PmReturn_t
plat_getByte(uint8_t *b)
{
    PmReturn_t retval = PM_RET_OK;

    if (no_usb) {
      panic(5);
    }

    // wait until there actually is data
    while (!plat_isDataAvail()) { }

    *b = (uint8_t) UARTCharGet(UART0_BASE);

    return retval;
}


tBoolean
plat_isDataAvail(void)
{
    tBoolean chars_avail;

    if (no_usb) {
      return false;
    }

    chars_avail = UARTCharsAvail(UART0_BASE);
    if (!chars_avail) {
      plat_cts(0);
    }

    return chars_avail;
}  


PmReturn_t
plat_putByte(uint8_t b)
{
    PmReturn_t retval = PM_RET_OK;

    if (!no_usb) {
        UARTCharPut(UART0_BASE,  b);
    }

    return retval;
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
    } else {
      obj_print(gVmGlobal.errObj, 0);
    }

    plat_putByte(0x1e);

    lib_printf("7");
    plat_putByte(0x1f);
    plat_printTrace();
    
    plat_putByte(0x1d);
}



