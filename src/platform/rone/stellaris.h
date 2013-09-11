/* platform/stellaris/stellaris.h
 *
 * Private headers used by the platform/ module but NOT called by the VM.
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

PmReturn_t plat_preinit(void);
void       plat_timer_start(void);
void       plat_timer_stop(void);
void       plat_cts(int value);
void       plat_profiler_tick(void);
void       panic(int blinks);

// for stack painting
#define STACK_COLOR 42

/* (r11) CTS Port/Pin */
#define CTS_SYSCTL_PORT    SYSCTL_PERIPH_GPIOC
#define CTS_GPIO_PORT      GPIO_PORTC_BASE
#define CTS_GPIO_PIN       GPIO_PIN_7

/* (r11) Heartbeat LED */
#define LED_SYSCTL_PORT    SYSCTL_PERIPH_GPIOE
#define LED_GPIO_PORT      GPIO_PORTE_BASE
#define LED_GPIO_PIN       GPIO_PIN_1

/* (r11) Switch Port/Pin */
#define SWITCH_SYSCTL_PORT SYSCTL_PERIPH_GPIOF
#define SWITCH_GPIO_PORT   GPIO_PORTF_BASE
#define SWITCH_GPIO_PIN    GPIO_PIN_1

/* (r11) FTDI sense Port/Pin */
#define USBSENSE_SYSCTL_PORT SYSCTL_PERIPH_GPIOB
#define USBSENSE_GPIO_PORT   GPIO_PORTB_BASE
#define USBSENSE_GPIO_PIN    GPIO_PIN_5

