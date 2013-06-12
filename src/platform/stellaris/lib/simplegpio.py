import sysctl, gpio

SYSCTL = {'a': sysctl.SYSCTL_PERIPH_GPIOA,
          'b': sysctl.SYSCTL_PERIPH_GPIOB,
          'c': sysctl.SYSCTL_PERIPH_GPIOC,
          'd': sysctl.SYSCTL_PERIPH_GPIOD,
          'e': sysctl.SYSCTL_PERIPH_GPIOE,
          'f': sysctl.SYSCTL_PERIPH_GPIOF,
          'g': sysctl.SYSCTL_PERIPH_GPIOG,
          'h': sysctl.SYSCTL_PERIPH_GPIOG,
          'j': sysctl.SYSCTL_PERIPH_GPIOJ}
          
PORTS  = {'a': gpio.GPIO_PORTA_BASE,
          'b': gpio.GPIO_PORTB_BASE,
          'c': gpio.GPIO_PORTC_BASE,
          'd': gpio.GPIO_PORTD_BASE,
          'e': gpio.GPIO_PORTE_BASE,
          'f': gpio.GPIO_PORTF_BASE,
          'g': gpio.GPIO_PORTG_BASE,
          'h': gpio.GPIO_PORTG_BASE,
          'j': gpio.GPIO_PORTJ_BASE}

PINS = {'0': gpio.GPIO_PIN_0,
        '1': gpio.GPIO_PIN_1,
        '2': gpio.GPIO_PIN_2,
        '3': gpio.GPIO_PIN_3,
        '4': gpio.GPIO_PIN_4,
        '5': gpio.GPIO_PIN_5,
        '6': gpio.GPIO_PIN_6,
        '7': gpio.GPIO_PIN_7}

INPUT = gpio.GPIO_PIN_TYPE_STD
PULLUP = gpio.GPIO_PIN_TYPE_STD_WPU
PULLDOWN = gpio.GPIO_PIN_TYPE_STD_WPD

def init_port(port):
    sysctl.SysCtlPeripheralEnable(SYSCTL[port])

class Output:
    def __init__(self, portpin):
        self.port = PORTS[portpin[0]]
        self.pin = PINS[portpin[1]]

        init_port(portpin[0])

        gpio.GPIOPinTypeGPIOOutput(self.port, self.pin)

    def write(self, value):
        if value:
            gpio.GPIOPinWrite(self.port, self.pin, self.pin)
        else:
            gpio.GPIOPinWrite(self.port, self.pin, 0)

    def off(self):
        self.write(False)

    def on(self):
        self.write(True)
            
class Input:
    def __init__(self, portpin, mode):
        self.port = PORTS[portpin[0]]
        self.pin = PINS[portpin[1]]
        
        init_port(portpin[0])

        gpio.GPIOPinTypeGPIOInput(self.port, self.pin)
        gpio.GPIOPadConfigSet(self.port, self.pin, gpio.GPIO_STRENGTH_2MA, mode)

    def read(self):
        if gpio.GPIOPinRead(self.port, self.pin):
            return True
        else:
            return False

