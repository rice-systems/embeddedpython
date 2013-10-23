/*
 * This file is part of the libopencm3 project.
 *
 * Copyright (C) 2010 Gareth McMullin <gareth@blacksphere.co.nz>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdlib.h>
#include <string.h>
#include <libopencm3/stm32/f4/rcc.h>
#include <libopencm3/stm32/f4/gpio.h>
#include <libopencm3/usb/usbd.h>
#include <libopencm3/usb/cdc.h>
#include <libopencm3/stm32/f4/nvic.h>

#include "cdcacm.h"

typedef struct 
{
  	int head;
  	int tail;
} buffer_status;

uint8_t *rxbuffer;
uint8_t *txbuffer;

buffer_status rxbuffer_status;

static int force_nak;

extern void delayus(uint32_t);

static const struct usb_device_descriptor dev = {
	.bLength = USB_DT_DEVICE_SIZE,
	.bDescriptorType = USB_DT_DEVICE,
	.bcdUSB = 0x0200,
	.bDeviceClass = USB_CLASS_CDC,
	.bDeviceSubClass = 0,
	.bDeviceProtocol = 0,
	.bMaxPacketSize0 = 64,
	.idVendor = 0x0483,
	.idProduct = 0x5740,
	.bcdDevice = 0x0200,
	.iManufacturer = 1,
	.iProduct = 2,
	.iSerialNumber = 3,
	.bNumConfigurations = 1,
};

/*
 * This notification endpoint isn't implemented. According to CDC spec it's
 * optional, but its absence causes a NULL pointer dereference in the
 * Linux cdc_acm driver.
 */
static const struct usb_endpoint_descriptor comm_endp[] = {{
	.bLength = USB_DT_ENDPOINT_SIZE,
	.bDescriptorType = USB_DT_ENDPOINT,
	.bEndpointAddress = 0x83,
	.bmAttributes = USB_ENDPOINT_ATTR_INTERRUPT,
	.wMaxPacketSize = 16,
	.bInterval = 255,
}};

static const struct usb_endpoint_descriptor data_endp[] = {{
	.bLength = USB_DT_ENDPOINT_SIZE,
	.bDescriptorType = USB_DT_ENDPOINT,
	.bEndpointAddress = 0x01,
	.bmAttributes = USB_ENDPOINT_ATTR_BULK,
	.wMaxPacketSize = 64,
	.bInterval = 1,
}, {
	.bLength = USB_DT_ENDPOINT_SIZE,
	.bDescriptorType = USB_DT_ENDPOINT,
	.bEndpointAddress = 0x82,
	.bmAttributes = USB_ENDPOINT_ATTR_BULK,
	.wMaxPacketSize = 64,
	.bInterval = 1,
}};

static const struct {
	struct usb_cdc_header_descriptor header;
	struct usb_cdc_call_management_descriptor call_mgmt;
	struct usb_cdc_acm_descriptor acm;
	struct usb_cdc_union_descriptor cdc_union;
} __attribute__((packed)) cdcacm_functional_descriptors = {
	.header = {
		.bFunctionLength = sizeof(struct usb_cdc_header_descriptor),
		.bDescriptorType = CS_INTERFACE,
		.bDescriptorSubtype = USB_CDC_TYPE_HEADER,
		.bcdCDC = 0x0110,
	},
	.call_mgmt = {
		.bFunctionLength =
			sizeof(struct usb_cdc_call_management_descriptor),
		.bDescriptorType = CS_INTERFACE,
		.bDescriptorSubtype = USB_CDC_TYPE_CALL_MANAGEMENT,
		.bmCapabilities = 0,
		.bDataInterface = 1,
	},
	.acm = {
		.bFunctionLength = sizeof(struct usb_cdc_acm_descriptor),
		.bDescriptorType = CS_INTERFACE,
		.bDescriptorSubtype = USB_CDC_TYPE_ACM,
		.bmCapabilities = 0,
	},
	.cdc_union = {
		.bFunctionLength = sizeof(struct usb_cdc_union_descriptor),
		.bDescriptorType = CS_INTERFACE,
		.bDescriptorSubtype = USB_CDC_TYPE_UNION,
		.bControlInterface = 0,
		.bSubordinateInterface0 = 1,
	 }
};

static const struct usb_interface_descriptor comm_iface[] = {{
	.bLength = USB_DT_INTERFACE_SIZE,
	.bDescriptorType = USB_DT_INTERFACE,
	.bInterfaceNumber = 0,
	.bAlternateSetting = 0,
	.bNumEndpoints = 1,
	.bInterfaceClass = USB_CLASS_CDC,
	.bInterfaceSubClass = USB_CDC_SUBCLASS_ACM,
	.bInterfaceProtocol = USB_CDC_PROTOCOL_AT,
	.iInterface = 0,

	.endpoint = comm_endp,

	.extra = &cdcacm_functional_descriptors,
	.extralen = sizeof(cdcacm_functional_descriptors)
}};

static const struct usb_interface_descriptor data_iface[] = {{
	.bLength = USB_DT_INTERFACE_SIZE,
	.bDescriptorType = USB_DT_INTERFACE,
	.bInterfaceNumber = 1,
	.bAlternateSetting = 0,
	.bNumEndpoints = 2,
	.bInterfaceClass = USB_CLASS_DATA,
	.bInterfaceSubClass = 0,
	.bInterfaceProtocol = 0,
	.iInterface = 0,

	.endpoint = data_endp,
}};

static const struct usb_interface ifaces[] = {{
	.num_altsetting = 1,
	.altsetting = comm_iface,
}, {
	.num_altsetting = 1,
	.altsetting = data_iface,
}};

static const struct usb_config_descriptor config = {
	.bLength = USB_DT_CONFIGURATION_SIZE,
	.bDescriptorType = USB_DT_CONFIGURATION,
	.wTotalLength = 0,
	.bNumInterfaces = 2,
	.bConfigurationValue = 1,
	.iConfiguration = 0,
	.bmAttributes = 0x80,
	.bMaxPower = 0x32,

	.interface = ifaces,
};

static const char *usb_strings[] = {
	"x",
	"Rice University",
	"CDC-ACM Demo",
	"DEMO",
};

/* Buffer for control requests */
uint8_t usbd_control_buffer[128];

/* USB device */
usbd_device *usbdev;

static int cdcacm_control_request(usbd_device *usbdev, 
        struct usb_setup_data *req, uint8_t **buf,
		uint16_t *len, 
        void (**complete)(usbd_device * usbd_dev, struct usb_setup_data *req))
{
	(void)complete;
	(void)buf;

	switch (req->bRequest) {
	case USB_CDC_REQ_SET_CONTROL_LINE_STATE: {
		/*
		 * This Linux cdc_acm driver requires this to be implemented
		 * even though it's optional in the CDC spec, and we don't
		 * advertise it in the ACM functional descriptor.
		 */
		return 1;
		}
	case USB_CDC_REQ_SET_LINE_CODING:
		if (*len < sizeof(struct usb_cdc_line_coding))
			return 0;

		return 1;
	}
	return 0;
}

int usbrx_dataAvail()
{
	int head = rxbuffer_status.head;
	int tail = rxbuffer_status.tail;
	if (head >= tail)
	{
		return head - tail;
	}
	else 
	{
		return USB_BUFFER_SIZE + 1 - (tail - head);
	}
}

int usbrx_spaceAvail()
{
	return USB_BUFFER_SIZE - usbrx_dataAvail(); 
}

void usb_setNak()
{
  	usbd_ep_nak_set(usbdev, 0x01, 1);
}

void usb_resetNak()
{
	if (force_nak == 0)
	{
		usbd_ep_nak_set(usbdev, 0x01, 0);
	}
}

static int rx_recv(void)
{
	int readlen = 0;
	int i;
	char buf[128];
	
	readlen = usbd_ep_read_packet(usbdev, 0x01, buf, 128);

	for (i = 0; i < readlen; i++)
	{
		rxbuffer[(rxbuffer_status.head+i) % (USB_BUFFER_SIZE+1)] = buf[i];
	}

	if (readlen)
	{
		rxbuffer_status.head += readlen;
		rxbuffer_status.head %= (USB_BUFFER_SIZE+1);
		if (usbrx_spaceAvail() < 128)
		{
			usb_setNak();
			force_nak = 1;
		}
	}
  	return readlen;
}

static void cdcacm_data_rx_cb(usbd_device *usbd_dev, uint8_t ep)
{
  	(void)ep;

  	rx_recv();
}

static void cdcacm_data_tx_cb(usbd_device *usbd_dev, uint8_t ep)
{
  	(void)ep;
  
}

static void cdcacm_set_config(usbd_device *usbd_dev, uint16_t wValue)
{
	(void)wValue;

	usbd_ep_setup(usbdev, 0x01, USB_ENDPOINT_ATTR_BULK, 64, cdcacm_data_rx_cb);
	usbd_ep_setup(usbdev, 0x82, USB_ENDPOINT_ATTR_BULK, 64, cdcacm_data_tx_cb);
	usbd_ep_setup(usbdev, 0x83, USB_ENDPOINT_ATTR_INTERRUPT, 16, NULL);

	usbd_register_control_callback(usbdev,
				USB_REQ_TYPE_CLASS | USB_REQ_TYPE_INTERFACE,
				USB_REQ_TYPE_TYPE | USB_REQ_TYPE_RECIPIENT,
				cdcacm_control_request);
}

int usbrx_getBytes(uint8_t *buf, int size) 
{
	int current_data_available = usbrx_dataAvail();
  	int read_data_size;
	int i;

	read_data_size = (size > current_data_available) ? current_data_available:size;

	for (i = 0; i < read_data_size; i++) {
    	buf[i] = rxbuffer[(rxbuffer_status.tail+i) % (USB_BUFFER_SIZE+1)];
  	}

  	rxbuffer_status.tail += read_data_size;
  	rxbuffer_status.tail %= (USB_BUFFER_SIZE+1);
  
	if (force_nak == 1)
	{
        delayus(5);
		if (usbrx_spaceAvail() >= 128)
		{
			force_nak = 0;
			usb_resetNak();
		}
	}
  
  	return read_data_size;
}

int usbtx_putBytes(uint8_t *buf, int size)
{
  	while (usbd_ep_write_packet(usbdev, 0x82, buf, size) == 0)
    	;

  	return size;
}

int usb_init(uint8_t *rx_buf, uint8_t *tx_buf)
{
  	rxbuffer = rx_buf;
  	txbuffer = tx_buf;
  
  	rxbuffer_status.head = 0;
  	rxbuffer_status.tail = 0;

	force_nak = 0;

	usbdev = usbd_init(&otgfs_usb_driver, &dev, &config, usb_strings, 4, 
                       usbd_control_buffer, sizeof(usbd_control_buffer));

	usbd_register_set_config_callback(usbdev, cdcacm_set_config);
  	nvic_enable_irq(NVIC_OTG_FS_IRQ);
  	return 0;
}

int stm32_usb_poll()
{
    usbd_poll(usbdev);
}
