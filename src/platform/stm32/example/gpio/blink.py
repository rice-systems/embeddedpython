import rcc # clock
import gpio
import sys

def init():
	print 'finished set up clock'

	# Enable GPIOD clock
	rcc.rcc_peripheral_enable_clock(rcc.RCC_AHB1_ENR, rcc.RCC_AHB1ENR_IOPDEN)

	# Enable to LED port and enable the LED pins as digital outputs
	gpio.gpio_mode_setup(gpio.GPIOD, gpio.GPIO_MODE_OUTPUT, gpio.GPIO_PUPD_NONE, gpio.GPIO12 | gpio.GPIO13 | gpio.GPIO14 | gpio.GPIO15)


def blink(num):
	gpio.gpio_clear(gpio.GPIOD, gpio.GPIO12 | gpio.GPIO13 | gpio.GPIO14 | gpio.GPIO15)

	for i in range(num):
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO12);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO12);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO13);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO13);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO14);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO14);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO15);
		sys.sleep(10)
		gpio.gpio_toggle(gpio.GPIOD, gpio.GPIO15);
		sys.sleep(10)

init()
print 'finished init'
blink(5)




