#ifndef CDCACM_H
#define CDCACM_H

#define USB_BUFFER_SIZE 512

int usb_init(uint8_t *rx_buf, uint8_t *tx_buf);
void usb_setNak(void);
void usb_resetNak(void);
int usbrx_getBytes(uint8_t *buf, int size);
int usbtx_putBytes(uint8_t *buf, int size);
int usbrx_dataAvail(void);
int usbrx_spaceAvail(void);

#endif
