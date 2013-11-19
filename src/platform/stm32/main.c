/* platform/main.c
 *
 * Starts the Owl VM.
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#include "gpio.h"
#include "pm.h"
#include "plat.h"
#include "stm32.h"
#include "usb/cdcacm.h"
#include "flash.h"

#define BLOCK_SIZE 1024
#define FLASH_IMG 1
#define BUILTIN_IMG 2
#define MAX_RETRIES 1

extern unsigned char usrlib_img[];
uint8_t *img_start;
extern unsigned int ticks;

int wait_for_command(void);
void load_image(void);
void echo(void);

void delayus(uint32_t);
void delay(uint32_t);
void blink(int blinks);

/* delay for nCount * 3 cycles */
void delay(uint32_t nCount) 
{
    __asm__("_delay_loop: subs r0, #1\n"
            "bne.n _delay_loop\n");
}

/* delay for nCount microseconds at 168MHz */
void delayus(uint32_t nCount)
{
    delay(nCount * 56);
}


void blink(int blinks) 
{
    // blink the light, scream and shout...
    int i;

    for (i=0; i<blinks; i++)
    {
        delayus(100000); //100ms
        // Turn all LEDs on
        gpio_toggle(GPIOD, GPIO12 | GPIO13 | GPIO14 | GPIO15);

        delayus(100000); //100ms
        gpio_toggle(GPIOD, GPIO12 | GPIO13 | GPIO14 | GPIO15);
          
    }
}


void panic(int nblinks) 
{
    while(1) 
    {
        blink(nblinks);
        delayus(1000000);
    }
}

void echo(void) 
{
    uint8_t data;
    PmReturn_t retval;

    while(1) 
    {
        retval = plat_getByte(&data);
        retval = plat_putByte(data);
    }
}


int wait_for_command(void) {
    PmReturn_t retval;
    uint8_t command;
  
    /* Get the image type */
    while (1) 
    {   
        if (gpio_get(GPIOA, GPIO0))
        {   
            while(gpio_get(GPIOA, GPIO0)) {}
            command = 'r';
            break;
        }
        if (plat_isDataAvail()) 
        {
            retval = plat_getByte(&command);
            if (retval != PM_RET_OK) 
            {
                panic(6); 
            }
            break;
        }
    }

    switch(command) {
    case 'l':
        gpio_toggle(GPIOD, GPIO12);
        load_image();
        return 0;
        break;
    case 'r':
        gpio_toggle(GPIOD, GPIO13);
        return FLASH_IMG;
        break;
    case 'i':
        gpio_toggle(GPIOD, GPIO14);
        return BUILTIN_IMG;
        break;
    case 'e':
        echo();
        break;
    default:
        panic(5);
        break;
    }	

    // shouldn't get here
    return 0;
}

void load_image(void) {

    uint8_t block[BLOCK_SIZE];
    uint8_t *block_destination = img_start;
    int i = 0;
    int finished = 0;
    int errors = 0;
    long program_results = 0;
    uint8_t hexbyte[2];

    PmReturn_t retval = PM_RET_OK;

    int image_size = 0;
    uint8_t checksum = 0;
    uint8_t *byte_to_check = img_start;

    // nak the usb to stop the host from sending data during flash operations
    usb_setNak();
    flash_clear_status_flags();
    flash_unlock();

    // erase sector 11
    flash_erase_sector((uint8_t)11, FLASH_CR_PROGRAM_X8);
    flash_wait_for_last_operation();
    flash_lock();
    usb_resetNak();

    // start reading the image
    while (!finished) 
    {
        plat_cts(1);
        memset(block, 0, BLOCK_SIZE);
        for (i=0; i<BLOCK_SIZE; i++) 
        {
            retval = plat_getByte(&hexbyte[0]);
            retval = plat_getByte(&hexbyte[1]);

            if (hexbyte[0] == 'x') 
            {
                finished++;
                break;
            } 
            else 
            {
                image_size++;
                block[i] = xtod_byte((char *) hexbyte);
            }
        }

        // write this block, prepare the next one
        // should check to see if we're within bounds of the flash size

        do 
        {
            if (errors > MAX_RETRIES) 
            {
                break;
            }

            plat_cts(1);
            usb_setNak();
            flash_clear_status_flags();
            flash_unlock();

            for (i=0; i<BLOCK_SIZE; i++)
            {
                flash_program_byte(block_destination+i, block[i]);
            }

            flash_lock();
            usb_resetNak();

            if (program_results != 0) {
                errors++;
            }
        } while (program_results != 0);

        block_destination += BLOCK_SIZE;
    }

    if (errors) 
    {
        lib_printf("e");
    } 
    else if (errors > MAX_RETRIES) 
    {
        lib_printf("f");
    } 
    else {
        lib_printf("s");
    }

    // calculate and echo the checksum back
    for (i=0; i<image_size; i++) {
        checksum ^= *byte_to_check;
        byte_to_check++;
    }

    lib_printf("%02x", checksum);
    blink(10);
}

int main(void)
{
    PmReturn_t retval;
    int image_to_run = 0;
    uint8_t image_offset = 0;

    retval = plat_preinit();
    img_start = (uint8_t *)(0x080E0000);

    PM_RETURN_IF_ERROR(retval);
    blink(2);

    while (!image_to_run) 
    {
        image_to_run = wait_for_command();
    }

    if (*img_start) {
        image_offset = *img_start;
    }

    if (image_to_run == FLASH_IMG) 
    {
        //before we run, make sure we actually have something to run
        if (!*img_start) 
        {
            panic(7);
        }

        retval = pm_init(img_start + image_offset);
        PM_RETURN_IF_ERROR(retval);
        
        retval = img_appendToPath((uint8_t *)usrlib_img);
        PM_RETURN_IF_ERROR(retval);
        
        /* Run the user program */
        retval = pm_run((char const *)(img_start) + 1);
    } 

    else
    {
        retval = pm_init((uint8_t *)usrlib_img);
        PM_RETURN_IF_ERROR(retval);

        if (*img_start) 
        {
            retval = img_appendToPath(img_start + image_offset);
            PM_RETURN_IF_ERROR(retval);
        }

        retval = pm_run("main");
    }
    return (int)retval;
}
