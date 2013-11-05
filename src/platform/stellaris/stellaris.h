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

// include the right headers for the part and library
#ifdef PART_LM3S9B92
#include "inc/lm3s9b92.h"
#include "inc/hw_ints.h"
#define LEGACY_STELLARISWARE
#endif

#ifdef PART_LM3S9D92
#include "inc/lm3s9d92.h"
#include "inc/hw_ints.h"
#define LEGACY_STELLARISWARE
#endif

#ifdef PART_TM4C123GH6PGE
#include "inc/tm4c123gh6pge.h"
#define TIVAWARE
#endif

#ifdef PART_TM4C129XNCZAD
#include "inc/tm4c129xnczad.h"
#define TIVAWARE
#endif

#ifdef PART_LM4F232H5QD
  /* LED Port/Pin */
  #define LED_SYSCTL_PORT    SYSCTL_PERIPH_GPIOG
  #define LED_GPIO_PORT      GPIO_PORTG_BASE
  #define LED_GPIO_PIN       GPIO_PIN_2
  
  /* Switch Port/Pin */
  #define SWITCH_SYSCTL_PORT SYSCTL_PERIPH_GPIOM
  #define SWITCH_GPIO_PORT   GPIO_PORTM_BASE
  #define SWITCH_GPIO_PIN    GPIO_PIN_4
#else
  /* LED Port/Pin */
  #define LED_SYSCTL_PORT    SYSCTL_PERIPH_GPIOD
  #define LED_GPIO_PORT      GPIO_PORTD_BASE
  #define LED_GPIO_PIN       GPIO_PIN_0
  
  /* Switch Port/Pin */
  #define SWITCH_SYSCTL_PORT SYSCTL_PERIPH_GPIOB
  #define SWITCH_GPIO_PORT   GPIO_PORTB_BASE
  #define SWITCH_GPIO_PIN    GPIO_PIN_4
#endif

/* USB select Port/Pin */
#define USBSEL_SYSCTL_PORT SYSCTL_PERIPH_GPIOB
#define USBSEL_GPIO_PORT   GPIO_PORTB_BASE
#define USBSEL_GPIO_PIN    GPIO_PIN_0

/* USB Host power supply Port/Pin */
#define USBPOW_SYSCTL_PORT SYSCTL_PERIPH_GPIOA
#define USBPOW_GPIO_PORT   GPIO_PORTA_BASE
#define USBPOW_GPIO_PIN    GPIO_PIN_6

