/* platform/stellaris/plat_stm32.c
 *
 * Supports the STM STM32F4 series parts.
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


/** Owl platform-specific routines for STM32 target */

#include "gpio.h"
#include "rcc.h"
#include "usb/cdcacm.h"
#include "libopencm3/cm3/systick.h"
#include "pm.h"
#include "plat.h"
#include "timer.h"
#include "stm32.h"
#include "libopencm3/cm3/nvic.h"

#define CALLBACK_MS 10
#define RESET_VAL 1000000000ul

unsigned char otg_fs_USBRxBuffer[USB_BUFFER_SIZE+1];
unsigned char otg_fs_USBTxBuffer[USB_BUFFER_SIZE+1];

unsigned int ticks = 0;

void ticker_callback(void);

#ifdef HAVE_BRIDGES
// table for bridge C subscribers
void (*c_subscriber_table[NUM_BRIDGE_C_SUBSCRIBERS]) (uint8_t bridge_index) = 
    { };
#endif

void
ticker_callback(void)
{
    PmReturn_t retval;

    ticks++;

    retval = pm_vmPeriodic(CALLBACK_MS * 1000);
    PM_REPORT_IF_ERROR(retval);
}

#ifdef HAVE_PROFILER
void
plat_profiler_tick(void)
{
    timer_clear_flag(TIM2, TIM_SR_UIF);
    profiler_tick();
}
#else
void
plat_profiler_tick(void)
{
    panic(10); // shouldn't happen
}
#endif

PmReturn_t
plat_preinit(void)
{
  
    rcc_clock_setup_hse_3v3(&hse_8mhz_3v3[CLOCK_3V3_168MHZ]);

    /* Enable GPIOD clock. */
    rcc_peripheral_enable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPDEN);
    rcc_peripheral_enable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPEEN);

    /* Enable GPIOA clock */
    rcc_peripheral_enable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPAEN);
    rcc_peripheral_enable_clock(&RCC_AHB2ENR, RCC_AHB1ENR_OTGHSEN);
    rcc_peripheral_enable_clock(&RCC_AHB2ENR, RCC_AHB2ENR_OTGFSEN);

    /*Enable to LED port and enable the LED pins as digital outputs*/
    gpio_mode_setup(GPIOD, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, 
                    GPIO12 | GPIO13 | GPIO14 | GPIO15);
    gpio_mode_setup(GPIOD, GPIO_MODE_INPUT, GPIO_PUPD_NONE, GPIO0);

    /*Enable the GPIO pin for the pushbutton as a digital input.*/
    gpio_mode_setup(GPIOA, GPIO_MODE_INPUT, GPIO_PUPD_NONE, GPIO0); 

    /*Enable the GPIO pin for the USB select and host power.*/
    gpio_mode_setup(GPIOA, GPIO_MODE_AF, GPIO_PUPD_NONE, 
                    GPIO9 | GPIO11 | GPIO12);
    gpio_set_af(GPIOA, GPIO_AF10, GPIO9 | GPIO11 | GPIO12);

    systick_set_clocksource(STK_CSR_CLKSOURCE_AHB_DIV8);
    usb_init(otg_fs_USBRxBuffer, otg_fs_USBTxBuffer);


#ifdef HAVE_PROFILER
    rcc_peripheral_enable_clock(&RCC_APB1ENR, RCC_APB1ENR_TIM2EN);
    timer_set_mode(TIM2, TIM_CR1_CKD_CK_INT,TIM_CR1_CMS_EDGE, 
                   TIM_CR1_DIR_DOWN);
    timer_set_prescaler(TIM2, 84000000/1000000);
    timer_set_period(TIM2, 100);
    nvic_enable_irq(NVIC_TIM2_IRQ);
    timer_enable_irq(TIM2, TIM_DIER_UIE);
    timer_clear_flag(TIM2, TIM_SR_UIF);
    timer_enable_counter(TIM2);
#endif

   return PM_RET_OK;

}

PmReturn_t
plat_setProfilerFrequency(int frequency) 
{

#ifdef HAVE_PROFILER
    timer_set_period(TIM2, 1000000 / frequency);
#endif

    return PM_RET_OK;
}


PmReturn_t
plat_init(void)
{
    systick_set_reload(168000000 / (1000 / CALLBACK_MS));
    systick_interrupt_enable();
    systick_counter_enable();

    return PM_RET_OK;
}


PmReturn_t
plat_deinit(void)
{
    // Is anything needed?
    return PM_RET_OK;
}


void 
plat_cts(int value)
{

}

PmReturn_t
plat_getByte(uint8_t *b)
{
    unsigned long ulRead;
    PmReturn_t retval = PM_RET_OK;

  	// Wait for data in the buffer
    while(!plat_isDataAvail()) ;
  
  	// Read byte
    ulRead = usbrx_getBytes((char *)b, 1);

    if (!ulRead)
    {
        PM_RAISE(retval, PM_RET_EX_IO);
    }        
  
    return retval;
}

uint8_t
plat_isDataAvail(void)
{
    int chars_avail;
    chars_avail = usbrx_dataAvail();
  
    return chars_avail ? 1 : 0;
}  

PmReturn_t
plat_putByte(uint8_t b)
{
    // write byte
    usbtx_putBytes(&b, 1);

    return PM_RET_OK;
}

PmReturn_t
plat_getMsTicks(uint32_t *r_ticks)
{
    // returns count from calls to pm_vmPeriodic()
    *r_ticks = pm_timerMsTicks;

    return PM_RET_OK;
}
