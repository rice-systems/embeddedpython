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

#include "pm.h"
#include "string.h"
#include "plat.h"

#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "inc/hw_gpio.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "tiva.h"

#if defined PART_TM4C129XNCZAD || defined PART_TM4C1294NCPDT
#define BLOCK_SIZE 16384
#else
#define BLOCK_SIZE 1024
#endif

#define FLASH_IMG 1
#define BUILTIN_IMG 2
#define MAX_RETRIES 1

int wait_for_command(void);
PmReturn_t load_image(void);
PmReturn_t echo(void);
void panic_temp(int);

extern unsigned char const usrlib_img[];
extern unsigned char _cookie;
extern unsigned int ticks;

void
panic(int blinks)
{
    // blink the light, scream and shout...
    int i;

    while(1)
    {
        for (i=0; i<blinks; i++)
        {
            SysCtlDelay(MAP_SysCtlClockGet() / 30); // 100ms
            // Turn LED on
            MAP_GPIOPinWrite(LED_GPIO_PORT, LED_GPIO_PIN, LED_GPIO_PIN);
            
            SysCtlDelay(MAP_SysCtlClockGet() / 30); 
            // Turn LED off
            MAP_GPIOPinWrite(LED_GPIO_PORT, LED_GPIO_PIN, 0x00);
        }
        
        SysCtlDelay(MAP_SysCtlClockGet() / 3); // 1000ms 
    }
}

void
panic_temp(int blinks)
{
    int i;

    for (i=0; i<blinks; i++)
    {
        // Turn LED on
        SysCtlDelay(MAP_SysCtlClockGet() / 10);
        MAP_GPIOPinWrite(LED_GPIO_PORT, LED_GPIO_PIN, LED_GPIO_PIN);
        
        // Turn LED off
        SysCtlDelay(MAP_SysCtlClockGet() / 10); 
        MAP_GPIOPinWrite(LED_GPIO_PORT, LED_GPIO_PIN, 0x00);
    }
        
    SysCtlDelay(MAP_SysCtlClockGet());
}

PmReturn_t
echo(void)
{
    uint8_t data;
    // TODO: should we check intermediate retvals?
    PmReturn_t retval;

    while(1)
    {
        retval = plat_getByte(&data);
        retval = plat_putByte(data);
    }
    return retval;
}

int
wait_for_command(void)
{
    PmReturn_t retval;
    uint8_t command;

    /* Get the image type */
    while (1)
    {
        if (!MAP_GPIOPinRead(SWITCH_GPIO_PORT, SWITCH_GPIO_PIN)) {
            command = 'r';
            while (!MAP_GPIOPinRead(SWITCH_GPIO_PORT, SWITCH_GPIO_PIN));
            // wait for the switch to debounce
            SysCtlDelay(MAP_SysCtlClockGet() / 30); 
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

    switch(command)
    {
        case 'l':
            load_image();
            return 0;
            break;
        case 'r':
            return FLASH_IMG;
            break;
        case 'i':
            return BUILTIN_IMG;
            break;
        case 'e':
            retval = echo();
            return retval;
            break;
        default:
            panic(5);
            break;
    }

    // shouldn't get here
    return 0;
}

PmReturn_t
load_image(void)
{
    uint8_t block[BLOCK_SIZE];
    uint8_t *block_destination = (uint8_t *)&(_cookie);
    PmReturn_t retval;
    int i;
    int finished = 0;
    int errors = 0;
    long program_results = 0;
    uint8_t hexbyte[2];

    int image_size = 0;
    uint8_t checksum = 0;
    uint8_t *byte_to_check = (uint8_t *)&(_cookie);

    // TODO: should we check intermediate retvals?
    // start reading the image
    while (!finished)
    {
        plat_cts(1);
        MAP_FlashErase((int)block_destination);
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
            else {
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
            program_results = MAP_FlashProgram((unsigned long *)block, 
                              (int)block_destination, BLOCK_SIZE);
      
            if (program_results != 0)
            {
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
    else
    {
        lib_printf("s");
    }

    // calculate and echo the checksum back
    for (i=0; i<image_size; i++)
    {
        checksum ^= *byte_to_check;
        byte_to_check++;
    }

    lib_printf("%02x", checksum);
    return retval;
}

int
main(void)
{
    PmReturn_t retval;
    int image_to_run = 0;
    uint8_t image_offset = 0;

    // first thing we want to do is paint the stack
    /*
    asm("mov %[result], sp" : [result] "=r" (sp) : );
    c = &__end;
    c++;
    while (c < sp) {
        *c = STACK_COLOR;
        c++;
    }
    */

    retval = plat_preinit();
    PM_RETURN_IF_ERROR(retval);

    while (!image_to_run) 
    {
        image_to_run = wait_for_command();
    }

    if (_cookie)
    {
      image_offset = _cookie;
    }

    if (image_to_run == FLASH_IMG) 
    {
        // before we run, make sure we actually have something to run
        if (!_cookie) 
        {
            panic(7);
        }

        retval = pm_init((uint8_t *)&_cookie + image_offset);
        PM_RETURN_IF_ERROR(retval);
        
        retval = img_appendToPath((uint8_t *)usrlib_img);
        PM_RETURN_IF_ERROR(retval);
        
        /* Run the user program */
        retval = pm_run((char const *)&_cookie + 1);
        
    } 
    else 
    {
        retval = pm_init((uint8_t *)usrlib_img);
        PM_RETURN_IF_ERROR(retval);
        
        if (_cookie) 
        {
            retval = img_appendToPath((uint8_t *)&_cookie + image_offset);
            PM_RETURN_IF_ERROR(retval);
        }
        
        /* Run the main program */
        retval = pm_run("main");
    }
    
    return (int)retval;
}
