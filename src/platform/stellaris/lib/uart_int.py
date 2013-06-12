"""__NATIVE__
#include "driverlib/uart.h"
#include "driverlib/interrupt.h"
#include "inc/hw_ints.h"

"""

def enable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    unsigned long ulStatus;
    
    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    lib_printf("initing UART interrupts...\n");

    ulStatus = UARTIntStatus(UART0_BASE, true);
    UARTIntClear(UART0_BASE, ulStatus);

    IntEnable(INT_UART0);
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

