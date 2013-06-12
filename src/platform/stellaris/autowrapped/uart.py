UART_CONFIG_WLEN_MASK = 0x00000060
UART_CONFIG_WLEN_8 = 0x00000060
UART_CONFIG_WLEN_7 = 0x00000040
UART_CONFIG_WLEN_6 = 0x00000020
UART_CONFIG_WLEN_5 = 0x00000000
UART_CONFIG_STOP_MASK = 0x00000008
UART_CONFIG_STOP_ONE = 0x00000000
UART_CONFIG_STOP_TWO = 0x00000008
UART_CONFIG_PAR_MASK = 0x00000086
UART_CONFIG_PAR_NONE = 0x00000000
UART_CONFIG_PAR_EVEN = 0x00000006
UART_CONFIG_PAR_ODD = 0x00000002
UART_CONFIG_PAR_ONE = 0x00000082
UART_CONFIG_PAR_ZERO = 0x00000086
UART_FIFO_TX1_8 = 0x00000000
UART_FIFO_TX2_8 = 0x00000001
UART_FIFO_TX4_8 = 0x00000002
UART_FIFO_TX6_8 = 0x00000003
UART_FIFO_TX7_8 = 0x00000004
UART_RXERROR_OVERRUN = 0x00000008
UART_RXERROR_BREAK = 0x00000004
UART_RXERROR_PARITY = 0x00000002
UART_RXERROR_FRAMING = 0x00000001
UART_OUTPUT_RTS = 0x00000800
UART_OUTPUT_DTR = 0x00000400
UART_INPUT_RI = 0x00000100
UART_INPUT_DCD = 0x00000004
UART_INPUT_DSR = 0x00000002
UART_INPUT_CTS = 0x00000001
UART_FLOWCONTROL_TX = 0x00008000
UART_FLOWCONTROL_RX = 0x00004000
UART_FLOWCONTROL_NONE = 0x00000000
UART_TXINT_MODE_FIFO = 0x00000000
UART_TXINT_MODE_EOT = 0x00000010
UART0_BASE = 0x4000C000
UART1_BASE = 0x4000D000
UART2_BASE = 0x4000E000
def UARTParityModeSet(ulBase, ulParity):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulParity;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulParity = ((pPmInt_t)p1)->val;

    UARTParityModeSet(ulBase, ulParity);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTParityModeGet(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTParityModeGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def UARTFIFOLevelSet(ulBase, ulTxLevel, ulRxLevel):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulTxLevel;
    unsigned long ulRxLevel;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulTxLevel = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulRxLevel = ((pPmInt_t)p2)->val;

    UARTFIFOLevelSet(ulBase, ulTxLevel, ulRxLevel);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTConfigSetExpClk(ulBase, ulUARTClk, ulBaud, ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulUARTClk;
    unsigned long ulBaud;
    unsigned long ulConfig;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 4)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulUARTClk = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulBaud = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulConfig = ((pPmInt_t)p3)->val;

    UARTConfigSetExpClk(ulBase, ulUARTClk, ulBaud, ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTEnable(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTDisable(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTDisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTFIFOEnable(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTFIFOEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTFIFODisable(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTFIFODisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTEnableSIR(ulBase, bLowPower):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    tBoolean bLowPower;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (p1 == PM_TRUE) {
        bLowPower = true;
    } else if (p1 == PM_FALSE) {
        bLowPower = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    UARTEnableSIR(ulBase, bLowPower);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTDisableSIR(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTDisableSIR(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTCharsAvail(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    tBoolean cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTCharsAvail(ulBase);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def UARTSpaceAvail(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    tBoolean cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTSpaceAvail(ulBase);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def UARTCharGetNonBlocking(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTCharGetNonBlocking(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def UARTCharGet(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTCharGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

def UARTCharGetForever(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    long cret;
    uint8_t outbyte;

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

    ulBase = ((pPmInt_t)p0)->val;

    while (1) {
        cret = UARTCharGet(ulBase);
        outbyte = cret;
        plat_putByte(outbyte);
    }

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

def UARTCharPutNonBlocking(ulBase, ucData):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned char ucData;

    pPmObj_t pret;
    tBoolean cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ucData = ((pPmInt_t)p1)->val;

    cret = UARTCharPutNonBlocking(ulBase, ucData);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def UARTCharPut(ulBase, ucData):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned char ucData;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ucData = ((pPmInt_t)p1)->val;

    UARTCharPut(ulBase, ucData);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

def UARTStringPut(ulBase, ucData):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned char ucData;
    uint16_t size, pos;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an string, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_STR)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    size = ((pPmString_t)p1)->length;

    for (pos=0; pos<size; pos++)
    {
        ucData = (((pPmString_t)p1)->val)[pos];
        UARTCharPut(ulBase, ucData);
    }

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass
    
def UARTBreakCtl(ulBase, bBreakState):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    tBoolean bBreakState;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (p1 == PM_TRUE) {
        bBreakState = true;
    } else if (p1 == PM_FALSE) {
        bBreakState = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    UARTBreakCtl(ulBase, bBreakState);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTBusy(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    tBoolean cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTBusy(ulBase);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def UARTRxErrorGet(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTRxErrorGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def UARTRxErrorClear(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTRxErrorClear(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTSmartCardEnable(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTSmartCardEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTSmartCardDisable(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

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

    ulBase = ((pPmInt_t)p0)->val;

    UARTSmartCardDisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTModemControlSet(ulBase, ulControl):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulControl;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulControl = ((pPmInt_t)p1)->val;

    UARTModemControlSet(ulBase, ulControl);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTModemControlClear(ulBase, ulControl):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulControl;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulControl = ((pPmInt_t)p1)->val;

    UARTModemControlClear(ulBase, ulControl);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTModemControlGet(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTModemControlGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def UARTModemStatusGet(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTModemStatusGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def UARTFlowControlSet(ulBase, ulMode):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulMode;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulMode = ((pPmInt_t)p1)->val;

    UARTFlowControlSet(ulBase, ulMode);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def UARTFlowControlGet(ulBase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    unsigned long ulBase;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    cret = UARTFlowControlGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
