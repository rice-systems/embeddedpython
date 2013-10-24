import rcc
import gpio
import spi

def setup_peripheral_clocks():
	print "setup peripheral clocks"

	# Enable SPI clock
	rcc.rcc_peripheral_enable_clock(rcc.RCC_AHB1_ENR, rcc.RCC_AHB1ENR_IOPAEN | rcc.RCC_AHB1ENR_IOPDEN | rcc.RCC_AHB1ENR_IOPEEN)
	rcc.rcc_peripheral_enable_clock(rcc.RCC_APB2_ENR, rcc.RCC_APB2ENR_SPI1EN)

	# Enable GPIOD clock
	rcc.rcc_peripheral_enable_clock(rcc.RCC_AHB1_ENR, rcc.RCC_AHB1ENR_IOPDEN)

def setup_gpio():
	print "setup gpio"
	# Enable to LED port and enable the LED pins as digital outputs
	gpio.gpio_mode_setup(gpio.GPIOD, gpio.GPIO_MODE_OUTPUT, gpio.GPIO_PUPD_NONE, gpio.GPIO12 | gpio.GPIO13 | gpio.GPIO14 | gpio.GPIO15)

def setup_spi():
	print "setup spi"
	# chip select
	gpio.gpio_mode_setup(gpio.GPIOE, gpio.GPIO_MODE_OUTPUT, gpio.GPIO_PUPD_NONE, gpio.GPIO3)

	# set to high which is not selected
	gpio.gpio_set(gpio.GPIOE, gpio.GPIO3)

	gpio.gpio_mode_setup(gpio.GPIOA, gpio.GPIO_MODE_AF, gpio.GPIO_PUPD_NONE, gpio.GPIO5 | gpio.GPIO6 | gpio.GPIO7)

	gpio.gpio_set_af(gpio.GPIOA, gpio.GPIO_AF5, gpio.GPIO5 | gpio.GPIO6 | gpio.GPIO7)

	spi.spi_disable_crc(spi.SPI1)
	spi.spi_init_master(spi.SPI1, spi.SPI_CR1_BAUDRATE_FPCLK_DIV_32, spi.SPI_CR1_CPOL_CLK_TO_1_WHEN_IDLE, spi.SPI_CR1_CPHA_CLK_TRANSITION_2, spi.SPI_CR1_DFF_8BIT, spi.SPI_CR1_MSBFIRST)

	spi.spi_enable_software_slave_management(spi.SPI1)
	spi.spi_set_nss_high(spi.SPI1)
	spi.spi_enable(spi.SPI1)

def send_command(command, data):
	gpio.gpio_clear(gpio.GPIOE, gpio.GPIO3)
	spi.spi_send(spi.SPI1, command)
	spi.spi_read(spi.SPI1)
	spi.spi_send(spi.SPI1, data)

	return_value = spi.spi_read(spi.SPI1)
	gpio.gpio_set(gpio.GPIOE, gpio.GPIO3)

	return return_value

def read_motion_axis(axis):
	data = 0
	command = (0x1 << 7) | (0x0 << 6) | (axis << 0)


	return send_command(command, data)

def read_motion():

	x = read_motion_axis(0x29)
	if (x > 4 and x < 60):
		gpio.gpio_set(gpio.GPIOD, gpio.GPIO15)
		gpio.gpio_clear(gpio.GPIOD, gpio.GPIO13)


	if (x > 208 and x < 252):
		gpio.gpio_set(gpio.GPIOD, gpio.GPIO13)
		gpio.gpio_clear(gpio.GPIOD, gpio.GPIO15)
	
	# print "x: " + str(x)
	y = read_motion_axis(0x2B)

	if (y > 4 and y < 60):
		gpio.gpio_set(gpio.GPIOD, gpio.GPIO14)
		gpio.gpio_clear(gpio.GPIOD, gpio.GPIO12)

	if (y > 208 and y < 252):
		gpio.gpio_set(gpio.GPIOD, gpio.GPIO12)
		gpio.gpio_clear(gpio.GPIOD, gpio.GPIO14)

	# print "y: " + str(y)


	# z = read_motion_axis(0x2D)
	# print "z: " + str(z)

	# combined = (x << 16) | (y << 8) | z

	# return combined

def setup_accelerometer():
	print "setup accelerometer"
	# READ bit not set | MS bit: when 0 do not increment address | bits 2-7 are address
	command = (0x0 << 7) | 	(0x0 << 6) | (0x20 << 0)
	# data rate selection, 1 = 400Hz | power down control, 1 = active | full scale selection 2G | Z axis enable | Y axis enable | X axis enable
	data = (0x1 << 7) | (0x1 << 6) | (0x0 << 5) | (0x1 << 2) | (0x1 << 1) | (0x1 << 0)

	send_command(command, data)


def main():
	setup_peripheral_clocks()
	setup_spi()
	setup_accelerometer()
	gpio.gpio_clear(gpio.GPIOD, gpio.GPIO12 | gpio.GPIO13 | gpio.GPIO14 | gpio.GPIO15)


	while(True):
		read_motion()

main()
