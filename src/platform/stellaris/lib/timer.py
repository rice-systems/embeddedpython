# high resolution timer support
r"""__NATIVE__
extern unsigned long plat_timer_stop_and_read(void);
"""

import simplegpio as gpio

def time():
    input = gpio.Input('d1', gpio.INPUT)
    out = gpio.Output('d0')

    out.off()

    # spin until input is high
    while input.read():
        pass

    res = _time()

    out.off()

    print res
    
def _time(port, pin):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmObj_t pret;
    unsigned long cret;

    // start the timer
    plat_timer_start();

    // drive the output line high
    GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_0, GPIO_PIN_0);

    // wait for the input line to go high
    while (GPIOPinRead(GPIO_PORTD_BASE, GPIO_PIN_1) == 0x0) { }

    // read the timer and return
    int_new(plat_timer_stop_and_read(), &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass
    
def start():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    // start the timer
    plat_timer_start();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass
    
def stop():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmObj_t pret;
    unsigned long cret;

    // read the timer and return
    int_new(plat_timer_stop_and_read(), &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

def test_timer():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    
    plat_timer_start();

    SysCtlDelay(1000);
    
    plat_timer_stop();

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    '''
    pass

