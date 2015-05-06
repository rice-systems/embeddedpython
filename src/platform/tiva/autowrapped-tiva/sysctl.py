# autowrapped header for stellaris/tiva
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "driverlib/sysctl.h"

'''

SYSCTL_PERIPH_ADC0 = 4026546176
SYSCTL_PERIPH_ADC1 = 4026546177
SYSCTL_PERIPH_CAN0 = 4026545152
SYSCTL_PERIPH_CAN1 = 4026545153
SYSCTL_PERIPH_CAN2 = 4026545154
SYSCTL_PERIPH_COMP0 = 4026547200
SYSCTL_PERIPH_COMP1 = 4026547201
SYSCTL_PERIPH_COMP2 = 4026547202
SYSCTL_PERIPH_EMAC0 = 4026571776
SYSCTL_PERIPH_EPHY0 = 4026544128
SYSCTL_PERIPH_EPI0 = 4026535936
SYSCTL_PERIPH_GPIOA = 4026533888
SYSCTL_PERIPH_GPIOB = 4026533889
SYSCTL_PERIPH_GPIOC = 4026533890
SYSCTL_PERIPH_GPIOD = 4026533891
SYSCTL_PERIPH_GPIOE = 4026533892
SYSCTL_PERIPH_GPIOF = 4026533893
SYSCTL_PERIPH_GPIOG = 4026533894
SYSCTL_PERIPH_GPIOH = 4026533895
SYSCTL_PERIPH_GPIOJ = 4026533896
SYSCTL_PERIPH_HIBERNATE = 4026536960
SYSCTL_PERIPH_CCM0 = 4026561536
SYSCTL_PERIPH_EEPROM0 = 4026554368
SYSCTL_PERIPH_FAN0 = 4026553344
SYSCTL_PERIPH_FAN1 = 4026553345
SYSCTL_PERIPH_GPIOK = 4026533897
SYSCTL_PERIPH_GPIOL = 4026533898
SYSCTL_PERIPH_GPIOM = 4026533899
SYSCTL_PERIPH_GPION = 4026533900
SYSCTL_PERIPH_GPIOP = 4026533901
SYSCTL_PERIPH_GPIOQ = 4026533902
SYSCTL_PERIPH_GPIOR = 4026533903
SYSCTL_PERIPH_GPIOS = 4026533904
SYSCTL_PERIPH_GPIOT = 4026533905
SYSCTL_PERIPH_I2C0 = 4026540032
SYSCTL_PERIPH_I2C1 = 4026540033
SYSCTL_PERIPH_I2C2 = 4026540034
SYSCTL_PERIPH_I2C3 = 4026540035
SYSCTL_PERIPH_I2C4 = 4026540036
SYSCTL_PERIPH_I2C5 = 4026540037
SYSCTL_PERIPH_I2C6 = 4026540038
SYSCTL_PERIPH_I2C7 = 4026540039
SYSCTL_PERIPH_I2C8 = 4026540040
SYSCTL_PERIPH_I2C9 = 4026540041
SYSCTL_PERIPH_LCD0 = 4026568704
SYSCTL_PERIPH_PWM0 = 4026548224
SYSCTL_PERIPH_PWM1 = 4026548225
SYSCTL_PERIPH_QEI0 = 4026549248
SYSCTL_PERIPH_QEI1 = 4026549249
SYSCTL_PERIPH_SSI0 = 4026539008
SYSCTL_PERIPH_SSI1 = 4026539009
SYSCTL_PERIPH_SSI2 = 4026539010
SYSCTL_PERIPH_SSI3 = 4026539011
SYSCTL_PERIPH_TIMER0 = 4026532864
SYSCTL_PERIPH_TIMER1 = 4026532865
SYSCTL_PERIPH_TIMER2 = 4026532866
SYSCTL_PERIPH_TIMER3 = 4026532867
SYSCTL_PERIPH_TIMER4 = 4026532868
SYSCTL_PERIPH_TIMER5 = 4026532869
SYSCTL_PERIPH_TIMER6 = 4026532870
SYSCTL_PERIPH_TIMER7 = 4026532871
SYSCTL_PERIPH_UART0 = 4026537984
SYSCTL_PERIPH_UART1 = 4026537985
SYSCTL_PERIPH_UART2 = 4026537986
SYSCTL_PERIPH_UART3 = 4026537987
SYSCTL_PERIPH_UART4 = 4026537988
SYSCTL_PERIPH_UART5 = 4026537989
SYSCTL_PERIPH_UART6 = 4026537990
SYSCTL_PERIPH_UART7 = 4026537991
SYSCTL_PERIPH_UDMA = 4026534912
SYSCTL_PERIPH_USB0 = 4026542080
SYSCTL_BOR_RESET = 2
SYSCTL_BOR_RESAMPLE = 1
SYSCTL_PWMDIV_1 = 0
SYSCTL_PWMDIV_2 = 1048576
SYSCTL_PWMDIV_4 = 1179648
SYSCTL_PWMDIV_8 = 1310720
SYSCTL_PWMDIV_16 = 1441792
SYSCTL_PWMDIV_32 = 1572864
SYSCTL_PWMDIV_64 = 1703936
SYSCTL_ADCSPEED_1MSPS = 3840
SYSCTL_ADCSPEED_500KSPS = 2560
SYSCTL_ADCSPEED_250KSPS = 1280
SYSCTL_ADCSPEED_125KSPS = 0
SYSCTL_INT_OSC_DIS = 2
SYSCTL_MAIN_OSC_DIS = 1

def SysCtlSRAMSizeGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlSRAMSizeGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlFlashSizeGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlFlashSizeGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlFlashSectorSizeGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlFlashSectorSizeGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlPeripheralPresent():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

    _Bool cret;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    cret = SysCtlPeripheralPresent(ui32Peripheral);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def SysCtlPeripheralReady():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

    _Bool cret;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    cret = SysCtlPeripheralReady(ui32Peripheral);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def SysCtlPeripheralPowerOn():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralPowerOn(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralPowerOff():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralPowerOff(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralReset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralReset(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralEnable(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralDisable(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralSleepEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralSleepEnable(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralSleepDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralSleepDisable(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralDeepSleepEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralDeepSleepEnable(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralDeepSleepDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Peripheral;

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

    ui32Peripheral = ((pPmInt_t)p0)->val;

    SysCtlPeripheralDeepSleepDisable(ui32Peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPeripheralClockGating():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    _Bool bEnable;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (p0 == PM_TRUE) {
        bEnable = true;
    } else if (p0 == PM_FALSE) {
        bEnable = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    SysCtlPeripheralClockGating(bEnable);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
# WARNING: unable to parse declaration of function SysCtlIntRegister. skipped.
def SysCtlIntUnregister():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    SysCtlIntUnregister();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlIntEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Ints;

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

    ui32Ints = ((pPmInt_t)p0)->val;

    SysCtlIntEnable(ui32Ints);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlIntDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Ints;

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

    ui32Ints = ((pPmInt_t)p0)->val;

    SysCtlIntDisable(ui32Ints);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlIntClear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Ints;

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

    ui32Ints = ((pPmInt_t)p0)->val;

    SysCtlIntClear(ui32Ints);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlIntStatus():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    _Bool bMasked;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    p0 = NATIVE_GET_LOCAL(0);

    /* If arg is not an int, raise TypeError */
    if (p0 == PM_TRUE) {
        bMasked = true;
    } else if (p0 == PM_FALSE) {
        bMasked = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    cret = SysCtlIntStatus(bMasked);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlLDOSleepSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Voltage;

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

    ui32Voltage = ((pPmInt_t)p0)->val;

    SysCtlLDOSleepSet(ui32Voltage);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlLDOSleepGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlLDOSleepGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlLDODeepSleepSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Voltage;

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

    ui32Voltage = ((pPmInt_t)p0)->val;

    SysCtlLDODeepSleepSet(ui32Voltage);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlLDODeepSleepGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlLDODeepSleepGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlSleepPowerSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlSleepPowerSet(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlDeepSleepPowerSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlDeepSleepPowerSet(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass
   

def SysCtlReset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
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

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    SysCtlSleep();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlDeepSleep():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    SysCtlDeepSleep();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlResetCauseGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlResetCauseGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlResetCauseClear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Causes;

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

    ui32Causes = ((pPmInt_t)p0)->val;

    SysCtlResetCauseClear(ui32Causes);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlDelay():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Count;

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

    ui32Count = ((pPmInt_t)p0)->val;

    SysCtlDelay(ui32Count);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlMOSCConfigSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlMOSCConfigSet(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPIOSCCalibrate():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Type;

    pPmInt_t pret;
    uint32_t cret;

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

    ui32Type = ((pPmInt_t)p0)->val;

    cret = SysCtlPIOSCCalibrate(ui32Type);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlClockSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlClockSet(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlClockGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlClockGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlDeepSleepClockSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlDeepSleepClockSet(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlDeepSleepClockConfigSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t ui32Div;
    uint32_t ui32Config;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
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

    ui32Div = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ui32Config = ((pPmInt_t)p1)->val;

    SysCtlDeepSleepClockConfigSet(ui32Div, ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPWMClockSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlPWMClockSet(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlPWMClockGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlPWMClockGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass
 
def SysCtlGPIOAHBEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32GPIOPeripheral;

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

    ui32GPIOPeripheral = ((pPmInt_t)p0)->val;

    SysCtlGPIOAHBEnable(ui32GPIOPeripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlGPIOAHBDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32GPIOPeripheral;

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

    ui32GPIOPeripheral = ((pPmInt_t)p0)->val;

    SysCtlGPIOAHBDisable(ui32GPIOPeripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlUSBPLLEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    SysCtlUSBPLLEnable();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlUSBPLLDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    SysCtlUSBPLLDisable();

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlClockFreqSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t ui32Config;
    uint32_t ui32SysClock;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
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

    ui32Config = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ui32SysClock = ((pPmInt_t)p1)->val;

    cret = SysCtlClockFreqSet(ui32Config, ui32SysClock);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

def SysCtlResetBehaviorSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Behavior;

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

    ui32Behavior = ((pPmInt_t)p0)->val;

    SysCtlResetBehaviorSet(ui32Behavior);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlResetBehaviorGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlResetBehaviorGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlClockOutConfig():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t ui32Config;
    uint32_t ui32Div;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 2)
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

    ui32Config = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ui32Div = ((pPmInt_t)p1)->val;

    SysCtlClockOutConfig(ui32Config, ui32Div);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlAltClkConfig():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlAltClkConfig(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlNMIStatus():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlNMIStatus();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlNMIClear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Status;

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

    ui32Status = ((pPmInt_t)p0)->val;

    SysCtlNMIClear(ui32Status);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlVoltageEventConfig():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Config;

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

    ui32Config = ((pPmInt_t)p0)->val;

    SysCtlVoltageEventConfig(ui32Config);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def SysCtlVoltageEventStatus():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    pPmInt_t pret;
    uint32_t cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = SysCtlVoltageEventStatus();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def SysCtlVoltageEventClear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t ui32Status;

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

    ui32Status = ((pPmInt_t)p0)->val;

    SysCtlVoltageEventClear(ui32Status);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
