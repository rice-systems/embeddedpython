"""__NATIVE__
typedef unsigned char tBoolean;

"""

SYSCTL_PERIPH_ADC0 = 0x00100001
SYSCTL_PERIPH_ADC1 = 0x00100002
SYSCTL_PERIPH_PWM = 0x00100010
SYSCTL_PERIPH_CAN0 = 0x00100100
SYSCTL_PERIPH_CAN1 = 0x00100200
SYSCTL_PERIPH_CAN2 = 0x00100400
SYSCTL_PERIPH_WDOG1 = 0x00101000
SYSCTL_PERIPH_UART0 = 0x10000001
SYSCTL_PERIPH_UART1 = 0x10000002
SYSCTL_PERIPH_UART2 = 0x10000004
SYSCTL_PERIPH_SSI0 = 0x10000010
SYSCTL_PERIPH_SSI1 = 0x10000020
SYSCTL_PERIPH_QEI0 = 0x10000100
SYSCTL_PERIPH_QEI1 = 0x10000200
SYSCTL_PERIPH_I2C0 = 0x10001000
SYSCTL_PERIPH_I2C1 = 0x10004000
SYSCTL_PERIPH_TIMER0 = 0x10100001
SYSCTL_PERIPH_TIMER1 = 0x10100002
SYSCTL_PERIPH_TIMER2 = 0x10100004
SYSCTL_PERIPH_TIMER3 = 0x10100008
SYSCTL_PERIPH_COMP0 = 0x10100100
SYSCTL_PERIPH_COMP1 = 0x10100200
SYSCTL_PERIPH_COMP2 = 0x10100400
SYSCTL_PERIPH_I2S0 = 0x10101000
SYSCTL_PERIPH_EPI0 = 0x10104000
SYSCTL_PERIPH_GPIOA = 0x20000001
SYSCTL_PERIPH_GPIOB = 0x20000002
SYSCTL_PERIPH_GPIOC = 0x20000004
SYSCTL_PERIPH_GPIOD = 0x20000008
SYSCTL_PERIPH_GPIOE = 0x20000010
SYSCTL_PERIPH_GPIOF = 0x20000020
SYSCTL_PERIPH_GPIOG = 0x20000040
SYSCTL_PERIPH_GPIOH = 0x20000080
SYSCTL_PERIPH_GPIOJ = 0x20000100
SYSCTL_PWMDIV_1 = 0x00000000
SYSCTL_PWMDIV_2 = 0x00100000
SYSCTL_PWMDIV_4 = 0x00120000
SYSCTL_PWMDIV_8 = 0x00140000
SYSCTL_PWMDIV_16 = 0x00160000
SYSCTL_PWMDIV_32 = 0x00180000
SYSCTL_PWMDIV_64 = 0x001A000
SYSCTL_ADCSPEED_1MSPS   = 0x00000F00
SYSCTL_ADCSPEED_500KSPS = 0x00000A00
SYSCTL_ADCSPEED_250KSPS = 0x00000500
SYSCTL_ADCSPEED_125KSPS = 0x00000000

def SysCtlReset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    SysCtlReset();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

def SysCtlSleep():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    SysCtlReset();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass


def SysCtlADCSpeedSet(ulSpeed):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulSpeed;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulSpeed = ((pPmInt_t)p0)->val;

    SysCtlADCSpeedSet(ulSpeed);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlResetCauseGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;

    pPmObj_t pret;
    unsigned long cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    cret = SysCtlResetCauseGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def SysCtlResetCauseClear(ulCauses):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulCauses;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulCauses = ((pPmInt_t)p0)->val;

    SysCtlResetCauseClear(ulCauses);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlBrownOutConfigSet(ulConfig, ulDelay):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulConfig;
    unsigned long ulDelay;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulConfig = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulDelay = ((pPmInt_t)p1)->val;

    SysCtlBrownOutConfigSet(ulConfig, ulDelay);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlDelay(ulCount):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulCount;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulCount = ((pPmInt_t)p0)->val;

    SysCtlDelay(ulCount);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlClockSet(ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulConfig;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulConfig = ((pPmInt_t)p0)->val;

    SysCtlClockSet(ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlClockGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;

    pPmObj_t pret;
    unsigned long cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }
    
    cret = SysCtlClockGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def SysCtlPWMClockSet(ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulConfig;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulConfig = ((pPmInt_t)p0)->val;

    SysCtlPWMClockSet(ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPWMClockGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;

    pPmObj_t pret;
    unsigned long cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    cret = SysCtlPWMClockGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass


def SysCtlPeripheralReset(ulPeripheral):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulPeripheral;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPeripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralReset(ulPeripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralEnable(ulPeripheral):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulPeripheral;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPeripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralEnable(ulPeripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralDisable(ulPeripheral):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulPeripheral;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p0) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPeripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralDisable(ulPeripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

