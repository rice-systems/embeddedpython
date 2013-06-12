I2C_INT_MASTER = 0x00000001
I2C_INT_SLAVE = 0x00000002
I2C_MASTER_CMD_SINGLE_SEND = 0x00000007
I2C_MASTER_CMD_SINGLE_RECEIVE = 0x00000007
I2C_MASTER_CMD_BURST_SEND_START = 0x00000003
I2C_MASTER_CMD_BURST_SEND_CONT = 0x00000001
I2C_MASTER_CMD_BURST_SEND_FINISH = 0x00000005
I2C_MASTER_CMD_BURST_SEND_ERROR_STOP = 0x00000004
I2C_MASTER_CMD_BURST_RECEIVE_START = 0x0000000b
I2C_MASTER_CMD_BURST_RECEIVE_CONT = 0x00000009
I2C_MASTER_CMD_BURST_RECEIVE_FINISH = 0x00000005
I2C_MASTER_CMD_BURST_RECEIVE_ERROR_STOP = 0x00000004
I2C_MASTER_ERR_NONE = 0
I2C_MASTER_ERR_ADDR_ACK = 0x00000004
I2C_MASTER_ERR_DATA_ACK = 0x00000008
I2C_MASTER_ERR_ARB_LOST = 0x00000010
I2C_SLAVE_ACT_NONE = 0
I2C_SLAVE_ACT_RREQ = 0x00000001
I2C_SLAVE_ACT_TREQ = 0x00000002
I2C_SLAVE_ACT_RREQ_FBR = 0x00000005
I2C_MASTER_MAX_RETRIES = 1000
I2C_SLAVE_INT_STOP = 0x00000004
I2C_SLAVE_INT_START = 0x00000002
I2C_SLAVE_INT_DATA = 0x00000001
I2C0_MASTER_BASE = 0x40020000
I2C0_SLAVE_BASE = 0x40020800
I2C1_MASTER_BASE = 0x40021000
I2C1_SLAVE_BASE = 0x40021800
def I2CMasterBusBusy(ulBase):
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

    cret = I2CMasterBusBusy(ulBase);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def I2CMasterBusy(ulBase):
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

    cret = I2CMasterBusy(ulBase);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def I2CMasterControl(ulBase, ulCmd):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulCmd;

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

    ulCmd = ((pPmInt_t)p1)->val;

    I2CMasterControl(ulBase, ulCmd);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterDataGet(ulBase):
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

    cret = I2CMasterDataGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def I2CMasterDataPut(ulBase, ucData):
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

    I2CMasterDataPut(ulBase, ucData);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterDisable(ulBase):
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

    I2CMasterDisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterEnable(ulBase):
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

    I2CMasterEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterErr(ulBase):
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

    cret = I2CMasterErr(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def I2CMasterInitExpClk(ulBase, ulI2CClk, bFast):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulI2CClk;
    tBoolean bFast;

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

    ulI2CClk = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (p2 == PM_TRUE) {
        bFast = true;
    } else if (p2 == PM_FALSE) {
        bFast = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    I2CMasterInitExpClk(ulBase, ulI2CClk, bFast);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterIntClear(ulBase):
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

    I2CMasterIntClear(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterIntDisable(ulBase):
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

    I2CMasterIntDisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterIntEnable(ulBase):
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

    I2CMasterIntEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CMasterIntStatus(ulBase, bMasked):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    tBoolean bMasked;

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
    if (p1 == PM_TRUE) {
        bMasked = true;
    } else if (p1 == PM_FALSE) {
        bMasked = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    cret = I2CMasterIntStatus(ulBase, bMasked);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def I2CMasterSlaveAddrSet(ulBase, ucSlaveAddr, bReceive):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned char ucSlaveAddr;
    tBoolean bReceive;

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

    ucSlaveAddr = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (p2 == PM_TRUE) {
        bReceive = true;
    } else if (p2 == PM_FALSE) {
        bReceive = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    I2CMasterSlaveAddrSet(ulBase, ucSlaveAddr, bReceive);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveDataGet(ulBase):
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

    cret = I2CSlaveDataGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def I2CSlaveDataPut(ulBase, ucData):
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

    I2CSlaveDataPut(ulBase, ucData);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveDisable(ulBase):
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

    I2CSlaveDisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveEnable(ulBase):
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

    I2CSlaveEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveInit(ulBase, ucSlaveAddr):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned char ucSlaveAddr;

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

    ucSlaveAddr = ((pPmInt_t)p1)->val;

    I2CSlaveInit(ulBase, ucSlaveAddr);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntClear(ulBase):
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

    I2CSlaveIntClear(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntDisable(ulBase):
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

    I2CSlaveIntDisable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntEnable(ulBase):
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

    I2CSlaveIntEnable(ulBase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntClearEx(ulBase, ulIntFlags):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulIntFlags;

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

    ulIntFlags = ((pPmInt_t)p1)->val;

    I2CSlaveIntClearEx(ulBase, ulIntFlags);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntDisableEx(ulBase, ulIntFlags):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulIntFlags;

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

    ulIntFlags = ((pPmInt_t)p1)->val;

    I2CSlaveIntDisableEx(ulBase, ulIntFlags);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntEnableEx(ulBase, ulIntFlags):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulIntFlags;

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

    ulIntFlags = ((pPmInt_t)p1)->val;

    I2CSlaveIntEnableEx(ulBase, ulIntFlags);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def I2CSlaveIntStatus(ulBase, bMasked):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    tBoolean bMasked;

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
    if (p1 == PM_TRUE) {
        bMasked = true;
    } else if (p1 == PM_FALSE) {
        bMasked = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    cret = I2CSlaveIntStatus(ulBase, bMasked);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def I2CSlaveIntStatusEx(ulBase, bMasked):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    tBoolean bMasked;

    pPmObj_t pret;
    unsigned long cret;

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
        bMasked = true;
    } else if (p1 == PM_FALSE) {
        bMasked = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    cret = I2CSlaveIntStatusEx(ulBase, bMasked);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def I2CSlaveStatus(ulBase):
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

    cret = I2CSlaveStatus(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
