/* platform/stellaris/usb/plat_usb.c
 *
 * Copyright 2013 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/usb.h"
#include "usblib/usblib.h"
#include "usblib/usb-ids.h"
#include "usblib/usbcdc.h"
#include "usblib/device/usbdevice.h"
#include "usblib/device/usbdcdc.h"

#define USB_BUFFER_SIZE 128

// prototypes
unsigned long usb_xmit_callback(void *pvCBData,
                                unsigned long ulEvent,
                                unsigned long ulMsgParam,
                                void *pvMsgData);

unsigned long usb_recv_callback(void *pvCBData,
                                unsigned long ulEvent,
                                unsigned long ulMsgParam,
                                void *pvMsgData);

unsigned long usb_control_callback(void *pvCBData,
                                   unsigned long ulEvent,
                                   unsigned long ulMsgValue,
                                   void *pvMsgData);

// externs redefined later
extern bool usb_connected;
extern tUSBDCDCDevice g_sCDCDevice;
extern const tUSBBuffer g_usb_recv_buffer;
extern const tUSBBuffer g_usb_xmit_buffer;

// uninitialized data
tCDCSerInstance g_sSerialInstance;
unsigned char g_usb_xmit_ringbuffer[USB_BUFFER_SIZE];
unsigned char g_usb_xmit_workspace[USB_BUFFER_WORKSPACE_SIZE];
unsigned char g_usb_recv_ringbuffer[USB_BUFFER_SIZE];
unsigned char g_usb_recv_workspace[USB_BUFFER_WORKSPACE_SIZE];
tLineCoding currentLineCoding;

/* Languages */
const unsigned char g_pLangDescriptor[] =
{
    4,
    USB_DTYPE_STRING,
    USBShort(USB_LANG_EN_US)
};

const unsigned char g_pManufacturerString[] =
{
    2 + (11 * 2),
    USB_DTYPE_STRING,
    'O', 0, 'w', 0, 'l', 0, ' ', 0, 'P', 0, 'r', 0, 'o', 0, 'j', 0,
    'e', 0, 'c', 0, 't', 0
};

const unsigned char g_pProductString[] =
{
    2 + (16 * 2),
    USB_DTYPE_STRING,
    'V', 0, 'i', 0, 'r', 0, 't', 0, 'u', 0, 'a', 0, 'l', 0, ' ', 0,
    'C', 0, 'o', 0, 'm', 0, ' ', 0, 'P', 0, 'o', 0, 'r', 0, 't', 0
};

const unsigned char g_pSerialNumberString[] =
{
    2 + (8 * 2),
    USB_DTYPE_STRING,
    '1', 0, '0', 0, '0', 0, '0', 0, '0', 0, '0', 0, '0', 0, '1', 0
};

const unsigned char g_pControlInterfaceString[] =
{
    2 + (21 * 2),
    USB_DTYPE_STRING,
    'A', 0, 'C', 0, 'M', 0, ' ', 0, 'C', 0, 'o', 0, 'n', 0, 't', 0,
    'r', 0, 'o', 0, 'l', 0, ' ', 0, 'I', 0, 'n', 0, 't', 0, 'e', 0,
    'r', 0, 'f', 0, 'a', 0, 'c', 0, 'e', 0
};

const unsigned char g_pConfigString[] =
{
    2 + (26 * 2),
    USB_DTYPE_STRING,
    'S', 0, 'e', 0, 'l', 0, 'f', 0, ' ', 0, 'P', 0, 'o', 0, 'w', 0,
    'e', 0, 'r', 0, 'e', 0, 'd', 0, ' ', 0, 'C', 0, 'o', 0, 'n', 0,
    'f', 0, 'i', 0, 'g', 0, 'u', 0, 'r', 0, 'a', 0, 't', 0, 'i', 0,
    'o', 0, 'n', 0
};

const unsigned char * const g_pStringDescriptors[] =
{
    g_pLangDescriptor,
    g_pManufacturerString,
    g_pProductString,
    g_pSerialNumberString,
    g_pControlInterfaceString,
    g_pConfigString
};

#define NUM_STRING_DESCRIPTORS (sizeof(g_pStringDescriptors) / \
                                sizeof(unsigned char *))

tUSBDCDCDevice g_sCDCDevice =
{

    USB_VID_STELLARIS, //USB_VID_YOUR_VENDOR_ID,
    0x42, //USB_PID_YOUR_PRODUCT_ID,
    0, //POWER_CONSUMPTION_mA,
    USB_CONF_ATTR_SELF_PWR, // bmAttributes
    usb_control_callback,
    (void *)&g_sCDCDevice,
    USBBufferEventCallback,
    (void *)&g_usb_recv_buffer,
    USBBufferEventCallback,
    (void *)&g_usb_xmit_buffer,
    g_pStringDescriptors, // defined above
    NUM_STRING_DESCRIPTORS, // also defined above
    &g_sSerialInstance // still defined above
};


unsigned long usb_control_callback(void *pvCBData,
                                   unsigned long ulEvent,
                                   unsigned long ulMsgValue,
                                   void *pvMsgData)
{

    switch(ulEvent)
    {
        case USB_EVENT_CONNECTED:
            // this may not be entirely necessary, but who knows.
            USBBufferFlush(&g_usb_xmit_buffer);
            USBBufferFlush(&g_usb_recv_buffer);

            usb_connected = true;
            break;

        case USB_EVENT_DISCONNECTED:
            USBDevDisconnect(USB0_BASE);
            
            usb_connected = false;
            break;

        case USB_EVENT_SUSPEND:
            break;

        case USB_EVENT_RESUME:
            break;

        case USBD_CDC_EVENT_SEND_BREAK:
            break;

        case USBD_CDC_EVENT_CLEAR_BREAK:
            break;

        case USBD_CDC_EVENT_SET_LINE_CODING:
            memcpy(&currentLineCoding, pvMsgData, sizeof(tLineCoding));
            break;

        case USBD_CDC_EVENT_GET_LINE_CODING:
            USBDCDSendDataEP0(0, (unsigned char *) &currentLineCoding, sizeof(tLineCoding));
            break;

        case USBD_CDC_EVENT_SET_CONTROL_LINE_STATE:
            break;
    }

    return 0;
}



unsigned long usb_xmit_callback(void *pvCBData,
                                unsigned long ulEvent,
                                unsigned long ulMsgParam,
                                void *pvMsgData)
{
    // the manual says that we might care about USB_EVENT_TX_COMPLETE
    return 0;
}

const tUSBBuffer g_usb_xmit_buffer = 
{
    true,
    usb_xmit_callback,
    NULL,
    USBDCDCPacketWrite,
    USBDCDCTxPacketAvailable,
    &g_sCDCDevice,
    g_usb_xmit_ringbuffer,
    USB_BUFFER_SIZE,
    g_usb_xmit_workspace
};

unsigned long usb_recv_callback(void *pvCBData,
                                unsigned long ulEvent,
                                unsigned long ulMsgParam,
                                void *pvMsgData)
{
    switch (ulEvent)
    {
        case USB_EVENT_RX_AVAILABLE:
            // do nothing. plat_getByte just reads the buffer directly.
            return 0;

        case USB_EVENT_DATA_REMAINING:
            return USBBufferDataAvailable(&g_usb_recv_buffer);

        default:
            return 0;
    }
}

const tUSBBuffer g_usb_recv_buffer = 
{
    false,
    usb_recv_callback,
    NULL,
    USBDCDCPacketRead,
    USBDCDCRxPacketAvailable,
    &g_sCDCDevice,
    g_usb_recv_ringbuffer,
    USB_BUFFER_SIZE,
    g_usb_recv_workspace
};

