
# autowrapped header file for p14p
# twb at edu dot rice


INT_GPIOA = 16
INT_GPIOB = 17
INT_GPIOC = 18
INT_GPIOD = 19
INT_GPIOE = 20
INT_UART0 = 21
INT_UART1 = 22
INT_SSI0 = 23
INT_I2C0 = 24
INT_PWM0_FAULT = 25
INT_PWM0_0 = 26
INT_PWM0_1 = 27
INT_PWM0_2 = 28
INT_QEI0 = 29
INT_ADC0SS0 = 30
INT_ADC0SS1 = 31
INT_ADC0SS2 = 32
INT_ADC0SS3 = 33
INT_WATCHDOG = 34
INT_TIMER0A = 35
INT_TIMER0B = 36
INT_TIMER1A = 37
INT_TIMER1B = 38
INT_TIMER2A = 39
INT_TIMER2B = 40
INT_COMP0 = 41
INT_COMP1 = 42
INT_COMP2 = 43
INT_SYSCTL = 44
INT_FLASH = 45
INT_GPIOF = 46
INT_GPIOG = 47
INT_GPIOH = 48
INT_UART2 = 49
INT_SSI1 = 50
INT_TIMER3A = 51
INT_TIMER3B = 52
INT_I2C1 = 53
INT_QEI1 = 54
INT_CAN0 = 55
INT_CAN1 = 56
INT_CAN2 = 57
INT_ETH = 58
INT_HIBERNATE = 59
INT_USB0 = 60
INT_PWM0_3 = 61
INT_UDMA = 62
INT_UDMAERR = 63
INT_ADC1SS0 = 64
INT_ADC1SS1 = 65
INT_ADC1SS2 = 66
INT_ADC1SS3 = 67
INT_I2S0 = 68
INT_EPI0 = 69
INT_GPIOJ = 70
INT_GPIOK = 71
INT_GPIOL = 72
INT_SSI2 = 73
INT_SSI3 = 74
INT_UART3 = 75
INT_UART4 = 76
INT_UART5 = 77
INT_UART6 = 78
INT_UART7 = 79
INT_I2C2 = 84
INT_I2C3 = 85
INT_TIMER4A = 86
INT_TIMER4B = 87
INT_TIMER5A = 108
INT_TIMER5B = 109
INT_WTIMER0A = 110
INT_WTIMER0B = 111
INT_WTIMER1A = 112
INT_WTIMER1B = 113
INT_WTIMER2A = 114
INT_WTIMER2B = 115
INT_WTIMER3A = 116
INT_WTIMER3B = 117
INT_WTIMER4A = 118
INT_WTIMER4B = 119
INT_WTIMER5A = 120
INT_WTIMER5B = 121
INT_SYSEXC = 122
INT_PECI0 = 123
INT_LPC0 = 124
INT_I2C4 = 125
INT_I2C5 = 126
INT_GPIOM = 127
INT_GPION = 128
INT_FAN0 = 130
INT_GPIOP0 = 132
INT_GPIOP1 = 133
INT_GPIOP2 = 134
INT_GPIOP3 = 135
INT_GPIOP4 = 136
INT_GPIOP5 = 137
INT_GPIOP6 = 138
INT_GPIOP7 = 139
INT_GPIOQ0 = 140
INT_GPIOQ1 = 141
INT_GPIOQ2 = 142
INT_GPIOQ3 = 143
INT_GPIOQ4 = 144
INT_GPIOQ5 = 145
INT_GPIOQ6 = 146
INT_GPIOQ7 = 147
INT_PWM1_0 = 150
INT_PWM1_1 = 151
INT_PWM1_2 = 152
INT_PWM1_3 = 153
INT_PWM1_FAULT = 154
def IntMasterEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t ;

    pPmObj_t pret;
    tBoolean cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = ROM_IntMasterEnable();

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def IntMasterDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t ;

    pPmObj_t pret;
    tBoolean cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = ROM_IntMasterDisable();

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def IntPriorityGroupingSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBits;

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

    ulBits = ((pPmInt_t)p0)->val;

    ROM_IntPriorityGroupingSet(ulBits);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def IntPriorityGroupingGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t ;

    pPmObj_t pret;
    unsigned long cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = ROM_IntPriorityGroupingGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def IntPrioritySet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulInterrupt;
    unsigned char ucPriority;

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

    ulInterrupt = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ucPriority = ((pPmInt_t)p1)->val;

    ROM_IntPrioritySet(ulInterrupt, ucPriority);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def IntPriorityGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulInterrupt;

    pPmObj_t pret;
    long cret;

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

    ulInterrupt = ((pPmInt_t)p0)->val;

    cret = ROM_IntPriorityGet(ulInterrupt);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def IntEnable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulInterrupt;

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

    ulInterrupt = ((pPmInt_t)p0)->val;

    ROM_IntEnable(ulInterrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def IntDisable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulInterrupt;

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

    ulInterrupt = ((pPmInt_t)p0)->val;

    ROM_IntDisable(ulInterrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
# skipping IntIsEnabled
def IntPendSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulInterrupt;

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

    ulInterrupt = ((pPmInt_t)p0)->val;

    IntPendSet(ulInterrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def IntPendClear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulInterrupt;

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

    ulInterrupt = ((pPmInt_t)p0)->val;

    IntPendClear(ulInterrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def IntPriorityMaskSet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulPriorityMask;

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

    ulPriorityMask = ((pPmInt_t)p0)->val;

    IntPriorityMaskSet(ulPriorityMask);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def IntPriorityMaskGet():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t ;

    pPmObj_t pret;
    unsigned long cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "incorrect number of arguments");
        return retval;
    }

    cret = IntPriorityMaskGet();

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
