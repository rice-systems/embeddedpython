"""__NATIVE__
#include "inc/hw_ethernet.h"
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/ethernet.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "driverlib/systick.h"

#define ETH_BUFFER_SIZE 1500

volatile uint8_t eth_buf[ETH_BUFFER_SIZE];

"""

def get():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pout;
    uint8_t *psrc;
    long packet_size;

    // we have to give pymite a pointer it can mangle
    psrc = &eth_buf;

    if (EthernetPacketAvail(ETH_BASE))
    {
        packet_size = EthernetPacketGet(ETH_BASE, &eth_buf, ETH_BUFFER_SIZE);
        retval = string_new(psrc, packet_size, &pout);
        NATIVE_SET_TOS(pout);
    }
    else
    {
        NATIVE_SET_TOS(PM_NONE);
    }

    return retval;
    '''
    pass

def put(s):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t ps;
    long packet_size, bytes_sent;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ps = NATIVE_GET_LOCAL(0);

    /* Raise TypeError if arg is not string of length 1 */
    if (OBJ_GET_TYPE(ps) != OBJ_TYPE_STR)

    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    packet_size = ((pPmString_t)ps)->length;

    bytes_sent = EthernetPacketPut(ETH_BASE, 
        (unsigned char *) ((pPmString_t)ps)->val, 
        packet_size);

    if (packet_size != bytes_sent) {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_VAL, "frame not sent (too long?)");
    }

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

def init():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    static struct uip_eth_addr sTempAddr;
    unsigned long ulUser0, ulUser1;
    unsigned long ulTemp;

    lib_printf("Reading the MAC address from the user registers.\n");
    
    ROM_FlashUserGet(&ulUser0, &ulUser1);
    if((ulUser0 == 0xffffffff) || (ulUser1 == 0xffffffff))
    {
        //
        // We should never get here.  This is an error if the MAC address has
        // not been programmed into the device.  Exit the program.
        //
        lib_printf("MAC Address Not Programmed! Dying...\n");
        while(1)
        {
        }
    }

    lib_printf("Enabling and Reseting the Ethernet Controller.\n");
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_ETH);
    ROM_SysCtlPeripheralReset(SYSCTL_PERIPH_ETH);

    lib_printf("Enabling Port F for Ethernet LEDs.\n");
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    GPIOPinConfigure(GPIO_PF2_LED1);
    GPIOPinConfigure(GPIO_PF3_LED0);
    GPIOPinTypeEthernetLED(GPIO_PORTF_BASE, GPIO_PIN_2 | GPIO_PIN_3);

    lib_printf("Initializing the Ethernet Controller\n");
    
    ROM_EthernetIntDisable(ETH_BASE, (ETH_INT_PHY | ETH_INT_MDIO |
                                      ETH_INT_RXER | ETH_INT_RXOF |
                                      ETH_INT_TX | ETH_INT_TXER | ETH_INT_RX));
    ulTemp = ROM_EthernetIntStatus(ETH_BASE, false);
    ROM_EthernetIntClear(ETH_BASE, ulTemp);

    lib_printf("Initializing the Ethernet Controller for operation.\n");
    
    ROM_EthernetInitExpClk(ETH_BASE, ROM_SysCtlClockGet());

    lib_printf("Configuring the Ethernet Controller for normal operation.\n");
    
    // - Full Duplex
    // - TX CRC Auto Generation
    // - TX Padding Enabled
    ROM_EthernetConfigSet(ETH_BASE, (ETH_CFG_TX_DPLXEN | ETH_CFG_TX_CRCEN |
                                     ETH_CFG_TX_PADEN));

    lib_printf("Waiting for Link\n");
    while((ROM_EthernetPHYRead(ETH_BASE, PHY_MR1) & 0x0004) == 0)
    {
    }
    lib_printf("Link Established\n");

    lib_printf("Enabling the Ethernet Controller.\n");
    ROM_EthernetEnable(ETH_BASE);

    //
    // Convert the 24/24 split MAC address from NV ram into a 32/16 split MAC
    // address needed to program the hardware registers, then program the MAC
    // address into the Ethernet Controller registers.
    //
    sTempAddr.addr[0] = ((ulUser0 >>  0) & 0xff);
    sTempAddr.addr[1] = ((ulUser0 >>  8) & 0xff);
    sTempAddr.addr[2] = ((ulUser0 >> 16) & 0xff);
    sTempAddr.addr[3] = ((ulUser1 >>  0) & 0xff);
    sTempAddr.addr[4] = ((ulUser1 >>  8) & 0xff);
    sTempAddr.addr[5] = ((ulUser1 >> 16) & 0xff);

    lib_printf("Programming MAC address.\n");
    
    ROM_EthernetMACAddrSet(ETH_BASE, (unsigned char *)&sTempAddr);

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

