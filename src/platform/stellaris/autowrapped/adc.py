ADC_BASE = 0x40038000
ADC_TRIGGER_PROCESSOR = 0x00000000
ADC_TRIGGER_COMP0 = 0x00000001
ADC_TRIGGER_COMP1 = 0x00000002
ADC_TRIGGER_COMP2 = 0x00000003
ADC_TRIGGER_EXTERNAL = 0x00000004
ADC_TRIGGER_TIMER = 0x00000005
ADC_TRIGGER_PWM0 = 0x00000006
ADC_TRIGGER_PWM1 = 0x00000007
ADC_TRIGGER_PWM2 = 0x00000008
ADC_TRIGGER_PWM3 = 0x00000009
ADC_TRIGGER_ALWAYS = 0x0000000F
ADC_CTL_TS = 0x00000080
ADC_CTL_IE = 0x00000040
ADC_CTL_END = 0x00000020
ADC_CTL_D = 0x00000010
ADC_CTL_CH0 = 0x00000000
ADC_CTL_CH1 = 0x00000001
ADC_CTL_CH2 = 0x00000002
ADC_CTL_CH3 = 0x00000003
ADC_CTL_CH4 = 0x00000004
ADC_CTL_CH5 = 0x00000005
ADC_CTL_CH6 = 0x00000006
ADC_CTL_CH7 = 0x00000007
ADC_CTL_CH8 = 0x00000008
ADC_CTL_CH9 = 0x00000009
ADC_CTL_CH10 = 0x0000000A
ADC_CTL_CH11 = 0x0000000B
ADC_CTL_CH12 = 0x0000000C
ADC_CTL_CH13 = 0x0000000D
ADC_CTL_CH14 = 0x0000000E
ADC_CTL_CH15 = 0x0000000F
ADC_CTL_CMP0 = 0x00080000
ADC_CTL_CMP1 = 0x00090000
ADC_CTL_CMP2 = 0x000A0000
ADC_CTL_CMP3 = 0x000B0000
ADC_CTL_CMP4 = 0x000C0000
ADC_CTL_CMP5 = 0x000D0000
ADC_CTL_CMP6 = 0x000E0000
ADC_CTL_CMP7 = 0x000F0000
ADC_COMP_TRIG_NONE = 0x00000000
ADC_COMP_TRIG_LOW_ALWAYS = 0x00001000
ADC_COMP_TRIG_LOW_ONCE = 0x00001100
ADC_COMP_TRIG_LOW_HALWAYS = 0x00001200
ADC_COMP_TRIG_LOW_HONCE = 0x00001300
ADC_COMP_TRIG_MID_ALWAYS = 0x00001400
ADC_COMP_TRIG_MID_ONCE = 0x00001500
ADC_COMP_TRIG_HIGH_ALWAYS = 0x00001C00
ADC_COMP_TRIG_HIGH_ONCE = 0x00001D00
ADC_COMP_TRIG_HIGH_HALWAYS = 0x00001E00
ADC_COMP_TRIG_HIGH_HONCE = 0x00001F00
ADC_COMP_INT_NONE = 0x00000000
ADC_COMP_INT_LOW_ALWAYS = 0x00000010
ADC_COMP_INT_LOW_ONCE = 0x00000011
ADC_COMP_INT_LOW_HALWAYS = 0x00000012
ADC_COMP_INT_LOW_HONCE = 0x00000013
ADC_COMP_INT_MID_ALWAYS = 0x00000014
ADC_COMP_INT_MID_ONCE = 0x00000015
ADC_COMP_INT_HIGH_ALWAYS = 0x0000001C
ADC_COMP_INT_HIGH_ONCE = 0x0000001D
ADC_COMP_INT_HIGH_HALWAYS = 0x0000001E
ADC_COMP_INT_HIGH_HONCE = 0x0000001F
ADC_TRIGGER_WAIT = 0x08000000
ADC_TRIGGER_SIGNAL = 0x80000000
ADC_PHASE_0 = 0x00000000
ADC_PHASE_22_5 = 0x00000001
ADC_PHASE_45 = 0x00000002
ADC_PHASE_67_5 = 0x00000003
ADC_PHASE_90 = 0x00000004
ADC_PHASE_112_5 = 0x00000005
ADC_PHASE_135 = 0x00000006
ADC_PHASE_157_5 = 0x00000007
ADC_PHASE_180 = 0x00000008
ADC_PHASE_202_5 = 0x00000009
ADC_PHASE_225 = 0x0000000A
ADC_PHASE_247_5 = 0x0000000B
ADC_PHASE_270 = 0x0000000C
ADC_PHASE_292_5 = 0x0000000D
ADC_PHASE_315 = 0x0000000E
ADC_PHASE_337_5 = 0x0000000F
ADC_REF_INT = 0x00000000
ADC_REF_EXT_3V = 0x00000001

def ADCIntUnregister(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCIntUnregister(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCIntDisable(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCIntDisable(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCIntEnable(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCIntEnable(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCIntStatus(ulBase, ulSequenceNum, bMasked):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulSequenceNum;
    tBoolean bMasked;

    pPmObj_t pret;
    unsigned long cret;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (p2 == PM_TRUE) {
        bMasked = true;
    } else if (p2 == PM_FALSE) {
        bMasked = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    cret = ADCIntStatus(ulBase, ulSequenceNum, bMasked);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def ADCIntClear(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCIntClear(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceEnable(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCSequenceEnable(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceDisable(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCSequenceDisable(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceConfigure(ulBase, ulSequenceNum, ulTrigger, ulPriority):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulSequenceNum;
    unsigned long ulTrigger;
    unsigned long ulPriority;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulTrigger = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulPriority = ((pPmInt_t)p3)->val;

    ADCSequenceConfigure(ulBase, ulSequenceNum, ulTrigger, ulPriority);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceStepConfigure(ulBase, ulSequenceNum, ulStep, ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulSequenceNum;
    unsigned long ulStep;
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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulStep = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulConfig = ((pPmInt_t)p3)->val;

    ADCSequenceStepConfigure(ulBase, ulSequenceNum, ulStep, ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceOverflow(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

    pPmObj_t pret;
    long cret;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    cret = ADCSequenceOverflow(ulBase, ulSequenceNum);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def ADCSequenceOverflowClear(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCSequenceOverflowClear(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceUnderflow(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

    pPmObj_t pret;
    long cret;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    cret = ADCSequenceUnderflow(ulBase, ulSequenceNum);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def ADCSequenceUnderflowClear(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCSequenceUnderflowClear(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSequenceDataGet(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

    pPmObj_t pret, ptup;
    unsigned long cret0 = 0;
    unsigned long cret1 = 0;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    // hard coded pointer here.
    cret0 = ADCSequenceDataGet(ulBase, ulSequenceNum, &cret1);

    retval = tuple_new(2, &ptup);
    PM_RETURN_IF_ERROR(retval);

    retval = int_new(cret0, &pret);
    PM_RETURN_IF_ERROR(retval);
    ((pPmTuple_t) ptup)->items[0] = pret;

    retval = int_new(cret1, &pret);
    PM_RETURN_IF_ERROR(retval);
    ((pPmTuple_t) ptup)->items[1] = pret;

    NATIVE_SET_TOS(ptup);

    return retval;
    '''
    pass

    
def ADCProcessorTrigger(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCProcessorTrigger(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSoftwareOversampleConfigure(ulBase, ulSequenceNum, ulFactor):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulSequenceNum;
    unsigned long ulFactor;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulFactor = ((pPmInt_t)p2)->val;

    ADCSoftwareOversampleConfigure(ulBase, ulSequenceNum, ulFactor);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCSoftwareOversampleStepConfigure(ulBase, ulSequenceNum, ulStep, ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulSequenceNum;
    unsigned long ulStep;
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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulStep = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulConfig = ((pPmInt_t)p3)->val;

    ADCSoftwareOversampleStepConfigure(ulBase, ulSequenceNum, ulStep, ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCHardwareOversampleConfigure(ulBase, ulFactor):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulFactor;

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

    ulFactor = ((pPmInt_t)p1)->val;

    ADCHardwareOversampleConfigure(ulBase, ulFactor);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCComparatorConfigure(ulBase, ulComp, ulConfig):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    unsigned long ulBase;
    unsigned long ulComp;
    unsigned long ulConfig;

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

    ulComp = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulConfig = ((pPmInt_t)p2)->val;

    ADCComparatorConfigure(ulBase, ulComp, ulConfig);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCComparatorRegionSet(ulBase, ulComp, ulLowRef, ulHighRef):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulComp;
    unsigned long ulLowRef;
    unsigned long ulHighRef;

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

    ulComp = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulLowRef = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    ulHighRef = ((pPmInt_t)p3)->val;

    ADCComparatorRegionSet(ulBase, ulComp, ulLowRef, ulHighRef);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCComparatorReset(ulBase, ulComp, bTrigger, bInterrupt):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    unsigned long ulBase;
    unsigned long ulComp;
    tBoolean bTrigger;
    tBoolean bInterrupt;

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

    ulComp = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (p2 == PM_TRUE) {
        bTrigger = true;
    } else if (p2 == PM_FALSE) {
        bTrigger = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (p3 == PM_TRUE) {
        bInterrupt = true;
    } else if (p3 == PM_FALSE) {
        bInterrupt = false;
    } else {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected True or False");
        return retval;
    }

    ADCComparatorReset(ulBase, ulComp, bTrigger, bInterrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCComparatorIntDisable(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCComparatorIntDisable(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCComparatorIntEnable(ulBase, ulSequenceNum):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulSequenceNum;

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

    ulSequenceNum = ((pPmInt_t)p1)->val;

    ADCComparatorIntEnable(ulBase, ulSequenceNum);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCComparatorIntStatus(ulBase):
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

    cret = ADCComparatorIntStatus(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def ADCComparatorIntClear(ulBase, ulStatus):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulStatus;

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

    ulStatus = ((pPmInt_t)p1)->val;

    ADCComparatorIntClear(ulBase, ulStatus);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCReferenceSet(ulBase, ulRef):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulRef;

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

    ulRef = ((pPmInt_t)p1)->val;

    ADCReferenceSet(ulBase, ulRef);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCReferenceGet(ulBase):
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

    cret = ADCReferenceGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
def ADCPhaseDelaySet(ulBase, ulPhase):
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    unsigned long ulBase;
    unsigned long ulPhase;

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

    ulPhase = ((pPmInt_t)p1)->val;

    ADCPhaseDelaySet(ulBase, ulPhase);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def ADCPhaseDelayGet(ulBase):
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

    cret = ADCPhaseDelayGet(ulBase);

    int_new(cret, &pret);
    NATIVE_SET_TOS(pret);

    return retval;
    '''
    pass

    
