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

/* LED Port/Pin */
#define LED_SYSCTL_PORT    SYSCTL_PERIPH_GPIOD
#define LED_GPIO_PORT      GPIO_PORTD_BASE
#define LED_GPIO_PIN       GPIO_PIN_0

/* Switch Port/Pin */
#define SWITCH_SYSCTL_PORT SYSCTL_PERIPH_GPIOB
#define SWITCH_GPIO_PORT   GPIO_PORTB_BASE
#define SWITCH_GPIO_PIN    GPIO_PIN_4


/* USB select Port/Pin */
#define USBSEL_SYSCTL_PORT SYSCTL_PERIPH_GPIOB
#define USBSEL_GPIO_PORT   GPIO_PORTB_BASE
#define USBSEL_GPIO_PIN    GPIO_PIN_0

/* USB Host power supply Port/Pin */
#define USBPOW_SYSCTL_PORT SYSCTL_PERIPH_GPIOA
#define USBPOW_GPIO_PORT   GPIO_PORTA_BASE
#define USBPOW_GPIO_PIN    GPIO_PIN_6

