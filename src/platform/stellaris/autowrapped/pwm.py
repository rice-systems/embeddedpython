"""__NATIVE__

"""


PWM_BASE = 0x40028000

PWM_GEN_MODE_DOWN = 0x00000000
PWM_GEN_MODE_UP_DOWN = 0x00000002
PWM_GEN_MODE_SYNC = 0x00000038
PWM_GEN_MODE_NO_SYNC = 0x00000000
PWM_GEN_MODE_DBG_RUN = 0x00000004
PWM_GEN_MODE_DBG_STOP = 0x00000000
PWM_GEN_MODE_FAULT_LATCHED = 0x00040000
PWM_GEN_MODE_FAULT_UNLATCHED = 0x00000000
PWM_GEN_MODE_FAULT_MINPER = 0x00020000
PWM_GEN_MODE_FAULT_NO_MINPER = 0x00000000
PWM_GEN_MODE_FAULT_EXT = 0x00010000
PWM_GEN_MODE_FAULT_LEGACY = 0x00000000
PWM_GEN_MODE_DB_NO_SYNC = 0x00000000
PWM_GEN_MODE_DB_SYNC_LOCAL = 0x0000A800
PWM_GEN_MODE_DB_SYNC_GLOBAL = 0x0000FC00
PWM_GEN_MODE_GEN_NO_SYNC = 0x00000000
PWM_GEN_MODE_GEN_SYNC_LOCAL = 0x00000280
PWM_GEN_MODE_GEN_SYNC_GLOBAL = 0x000003C0
PWM_TR_CNT_ZERO = 0x00000100
PWM_TR_CNT_LOAD = 0x00000200
PWM_TR_CNT_AU = 0x00000400
PWM_TR_CNT_AD = 0x00000800
PWM_TR_CNT_BU = 0x00001000
PWM_TR_CNT_BD = 0x00002000
PWM_GEN_0 = 0x00000040
PWM_GEN_1 = 0x00000080
PWM_GEN_2 = 0x000000C0
PWM_GEN_3 = 0x00000100
PWM_GEN_0_BIT = 0x00000001
PWM_GEN_1_BIT = 0x00000002
PWM_GEN_2_BIT = 0x00000004
PWM_GEN_3_BIT = 0x00000008
PWM_GEN_EXT_0 = 0x00000800
PWM_GEN_EXT_1 = 0x00000880
PWM_GEN_EXT_2 = 0x00000900
PWM_GEN_EXT_3 = 0x00000980
PWM_OUT_0 = 0x00000040
PWM_OUT_1 = 0x00000041
PWM_OUT_2 = 0x00000082
PWM_OUT_3 = 0x00000083
PWM_OUT_4 = 0x000000C4
PWM_OUT_5 = 0x000000C5
PWM_OUT_6 = 0x00000106
PWM_OUT_7 = 0x00000107
PWM_OUT_0_BIT = 0x00000001
PWM_OUT_1_BIT = 0x00000002
PWM_OUT_2_BIT = 0x00000004
PWM_OUT_3_BIT = 0x00000008
PWM_OUT_4_BIT = 0x00000010
PWM_OUT_5_BIT = 0x00000020
PWM_OUT_6_BIT = 0x00000040
PWM_OUT_7_BIT = 0x00000080

def PWMGenConfigure(ulBase, ulGen, ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulGen;
    unsigned long ulConfig;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulConfig = ((pPmInt_t)p2)->val;

    PWMGenConfigure(ulBase, ulGen, ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMGenPeriodSet(ulBase, ulGen, ulPeriod):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulGen;
    unsigned long ulPeriod;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPeriod = ((pPmInt_t)p2)->val;

    PWMGenPeriodSet(ulBase, ulGen, ulPeriod);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMGenPeriodGet(ulBase, ulGen):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulGen;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    cret = PWMGenPeriodGet(ulBase, ulGen);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def PWMGenEnable(ulBase, ulGen):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulGen;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    PWMGenEnable(ulBase, ulGen);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMGenDisable(ulBase, ulGen):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulGen;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    PWMGenDisable(ulBase, ulGen);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMPulseWidthSet(ulBase, ulPWMOut, ulWidth):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulPWMOut;
    unsigned long ulWidth;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPWMOut = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulWidth = ((pPmInt_t)p2)->val;

    PWMPulseWidthSet(ulBase, ulPWMOut, ulWidth);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMPulseWidthGet(ulBase, ulPWMOut):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulPWMOut;

    pPmObj_t pret;
    unsigned long cret;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPWMOut = ((pPmInt_t)p1)->val;

    cret = PWMPulseWidthGet(ulBase, ulPWMOut);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def PWMDeadBandEnable(ulBase, ulGen, usRise, usFall):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulGen;
    unsigned short usRise;
    unsigned short usFall;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 4)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    usRise = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    usFall = ((pPmInt_t)p3)->val;

    PWMDeadBandEnable(ulBase, ulGen, usRise, usFall);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMDeadBandDisable(ulBase, ulGen):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulGen;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGen = ((pPmInt_t)p1)->val;

    PWMDeadBandDisable(ulBase, ulGen);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMSyncUpdate(ulBase, ulGenBits):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulGenBits;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGenBits = ((pPmInt_t)p1)->val;

    PWMSyncUpdate(ulBase, ulGenBits);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMSyncTimeBase(ulBase, ulGenBits):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulGenBits;

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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulGenBits = ((pPmInt_t)p1)->val;

    PWMSyncTimeBase(ulBase, ulGenBits);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMOutputState(ulBase, ulPWMOutBits, bEnable):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulPWMOutBits;
    tBoolean bEnable;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPWMOutBits = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    bEnable = ((pPmInt_t)p2)->val;

    PWMOutputState(ulBase, ulPWMOutBits, bEnable);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMOutputInvert(ulBase, ulPWMOutBits, bInvert):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulPWMOutBits;
    tBoolean bInvert;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPWMOutBits = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    bInvert = ((pPmInt_t)p2)->val;

    PWMOutputInvert(ulBase, ulPWMOutBits, bInvert);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMOutputFaultLevel(ulBase, ulPWMOutBits, bDriveHigh):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulPWMOutBits;
    tBoolean bDriveHigh;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPWMOutBits = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    bDriveHigh = ((pPmInt_t)p2)->val;

    PWMOutputFaultLevel(ulBase, ulPWMOutBits, bDriveHigh);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def PWMOutputFault(ulBase, ulPWMOutBits, bFaultSuppress):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulPWMOutBits;
    tBoolean bFaultSuppress;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
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

    ulBase = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    ulPWMOutBits = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    bFaultSuppress = ((pPmInt_t)p2)->val;

    PWMOutputFault(ulBase, ulPWMOutBits, bFaultSuppress);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass
