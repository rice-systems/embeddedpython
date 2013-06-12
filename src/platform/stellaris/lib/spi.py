r"""__NATIVE__
//#include "inc/hw_types.h"
#include "inc/hw_ethernet.h"
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/ethernet.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "driverlib/systick.h"
#include "driverlib/ssi.h"

/* GPIO for SPI */
#define SPI_SSI_BASE            SSI0_BASE
#define SPI_SSI_SYSCTL_PERIPH   SYSCTL_PERIPH_SSI0
#define SPI_GPIO_PORT_BASE      GPIO_PORTA_BASE
#define SPI_GPIO_SYSCTL_PERIPH  SYSCTL_PERIPH_GPIOA
#define SPI_SSI_CLK             GPIO_PIN_2
#define SPI_SSI_TX              GPIO_PIN_5
#define SPI_SSI_RX              GPIO_PIN_4

#define SPI_SSI_PINS            (SPI_SSI_TX | SPI_SSI_RX | SPI_SSI_CLK)
"""

import gpio
import sysctl

def init_cs(periph, port, pin):
    sysctl.SysCtlPeripheralEnable(periph)
    gpio.GPIOPinTypeGPIOOutput(port, pin)
    gpio.GPIOPadConfigSet(port, pin, gpio.GPIO_STRENGTH_4MA, gpio.GPIO_PIN_TYPE_STD_WPU)
    gpio.GPIOPinWrite(port, pin, pin)

def select(port, pin):
    gpio.GPIOPinWrite(port, pin, 0)
    
def deselect(port, pin):
    gpio.GPIOPinWrite(port, pin, pin)
    
def init():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    lib_printf("Initializing SPI...\n");
    
    /* Enable the peripherals used to drive the SDC on SSI */
    SysCtlPeripheralEnable(SPI_SSI_SYSCTL_PERIPH);
    SysCtlPeripheralEnable(SPI_GPIO_SYSCTL_PERIPH);

    /*
     * Configure the appropriate pins to be SSI instead of GPIO. The CS
     * signal is directly driven to ensure that we can hold it low through a
     * complete transaction with the SD card.
     */
    GPIOPinTypeSSI(SPI_GPIO_PORT_BASE, SPI_SSI_TX | SPI_SSI_RX | SPI_SSI_CLK);
    GPIOPadConfigSet(SPI_GPIO_PORT_BASE, SPI_SSI_PINS, GPIO_STRENGTH_4MA,
                     GPIO_PIN_TYPE_STD_WPU);

    /* Configure the SSI0 port */
    SSIConfigSetExpClk(SPI_SSI_BASE, SysCtlClockGet(), SSI_FRF_MOTO_MODE_0,
                       SSI_MODE_MASTER, 400000, 8);
    SSIEnable(SPI_SSI_BASE);

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def read():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t pbyte;
    uint32_t rcvdat;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    SSIDataPut(SPI_SSI_BASE, 0xFF); /* write dummy data */
    SSIDataGet(SPI_SSI_BASE, &rcvdat); /* read data from rx fifo */
    
    retval = int_new(rcvdat, &pbyte);
    PM_RETURN_IF_ERROR(retval);
    
    NATIVE_SET_TOS((pPmObj_t)pbyte);
    return retval;
    '''
    pass

def write(data):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pdata;
    uint32_t rcvdat;
    int16_t  i;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    pdata = (pPmInt_t) NATIVE_GET_LOCAL(0);

    /* Allow either a byte (within an INT) or a string of bytes */
    if (OBJ_GET_TYPE(pdata) == OBJ_TYPE_INT)
    {
        if (((pPmInt_t)pdata)->val > 255)
        {
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "expected byte");
            return retval;
        }
        /* Write the data to the tx fifo */
        SSIDataPut(SPI_SSI_BASE, ((pPmInt_t)pdata)->val); 
        /* flush data read during the write */
        SSIDataGet(SPI_SSI_BASE, &rcvdat);
    }
    else if (OBJ_GET_TYPE(pdata) == OBJ_TYPE_STR)
    {
        for (i=0; i<((pPmString_t)pdata)->length; i++)
        {
            /* Write the data to the tx fifo */
            SSIDataPut(SPI_SSI_BASE, ((pPmString_t)pdata)->val[i]); 
            /* flush data read during the write */
            SSIDataGet(SPI_SSI_BASE, &rcvdat);            
        }
    }
    else
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int or string");
        return retval;
    }

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def set_speed(s):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t pspeed;
    uint32_t speed;
    uint32_t maxspeed;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() > 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    maxspeed = SysCtlClockGet() / 2;
    if (maxspeed > 6250000)
    {
        maxspeed = 6250000;
    }

    if (NATIVE_GET_NUM_ARGS() == 1)
    {
        pspeed = (pPmInt_t) NATIVE_GET_LOCAL(0);
        /* If arg is not an int, raise TypeError */
        if (OBJ_GET_TYPE(pspeed) != OBJ_TYPE_INT)
        {
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
            return retval;
        }
        speed = pspeed->val;
        if (speed > maxspeed)
        {
            PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "argument exceeds maximum speed");
            return retval;
        }
    }
    else
    {
        speed = maxspeed;
    }

    SSIDisable(SPI_SSI_BASE);
    SSIConfigSetExpClk(SPI_SSI_BASE, SysCtlClockGet(), SSI_FRF_MOTO_MODE_0,
                       SSI_MODE_MASTER, speed, 8);
    SSIEnable(SPI_SSI_BASE);
    
    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass
    
