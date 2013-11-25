# autowrapped header for stm32
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "timer.h"

'''
TIM1 = 1073807360
TIM2 = 1073741824
TIM3 = 1073742848
TIM4 = 1073743872
TIM5 = 1073744896
TIM6 = 1073745920
TIM7 = 1073746944
TIM8 = 1073808384
TIM_CR1_CKD_CK_INT = 0
TIM_CR1_CKD_CK_INT_MUL_2 = 256
TIM_CR1_CKD_CK_INT_MUL_4 = 512
TIM_CR1_CKD_CK_INT_MASK = 768
TIM_CR1_ARPE = 128
TIM_CR1_CMS_EDGE = 0
TIM_CR1_CMS_CENTER_1 = 32
TIM_CR1_CMS_CENTER_2 = 64
TIM_CR1_CMS_CENTER_3 = 96
TIM_CR1_CMS_MASK = 96
TIM_CR1_DIR_UP = 0
TIM_CR1_DIR_DOWN = 16
TIM_CR1_OPM = 8
TIM_CR1_URS = 4
TIM_CR1_UDIS = 2
TIM_CR1_CEN = 1
TIM_CR2_OIS4 = 16384
TIM_CR2_OIS3N = 8192
TIM_CR2_OIS3 = 4096
TIM_CR2_OIS2N = 2048
TIM_CR2_OIS2 = 1024
TIM_CR2_OIS1N = 512
TIM_CR2_OIS1 = 256
TIM_CR2_OIS_MASK = 32512
TIM_CR2_TI1S = 128
TIM_CR2_MMS_RESET = 0
TIM_CR2_MMS_ENABLE = 16
TIM_CR2_MMS_UPDATE = 32
TIM_CR2_MMS_COMPARE_PULSE = 48
TIM_CR2_MMS_COMPARE_OC1REF = 64
TIM_CR2_MMS_COMPARE_OC2REF = 80
TIM_CR2_MMS_COMPARE_OC3REF = 96
TIM_CR2_MMS_COMPARE_OC4REF = 112
TIM_CR2_MMS_MASK = 112
TIM_CR2_CCDS = 8
TIM_CR2_CCUS = 4
TIM_CR2_CCPC = 1
TIM_OC1 = 0
TIM_OC1N = 1
TIM_OC2 = 2
TIM_OC2N = 3
TIM_OC3 = 4
TIM_OC3N = 5
TIM_OC4 = 6
TIM_OCM_FROZEN = 0
TIM_OCM_ACTIVE = 1
TIM_OCM_INACTIVE = 2
TIM_OCM_TOGGLE = 3
TIM_OCM_FORCE_LOW = 4
TIM_OCM_FORCE_HIGH = 5
TIM_OCM_PWM1 = 6
TIM_OCM_PWM2 = 7
TIM_IC1 = 0
TIM_IC2 = 1
TIM_IC3 = 2
TIM_IC4 = 3
TIM_IC_OFF = 0
TIM_IC_CK_INT_N_2 = 1
TIM_IC_CK_INT_N_4 = 2
TIM_IC_CK_INT_N_8 = 3
def timer_reset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_reset(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_irq():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t irq;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    irq = ((pPmInt_t)p1)->val;

    timer_enable_irq(timer_peripheral, irq);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_irq():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t irq;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    irq = ((pPmInt_t)p1)->val;

    timer_disable_irq(timer_peripheral, irq);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_interrupt_source():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t flag;

    _Bool cret;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    flag = ((pPmInt_t)p1)->val;

    cret = timer_interrupt_source(timer_peripheral, flag);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def timer_get_flag():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t flag;

    _Bool cret;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    flag = ((pPmInt_t)p1)->val;

    cret = timer_get_flag(timer_peripheral, flag);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def timer_clear_flag():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t flag;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    flag = ((pPmInt_t)p1)->val;

    timer_clear_flag(timer_peripheral, flag);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    uint32_t timer_peripheral;
    uint32_t clock_div;
    uint32_t alignment;
    uint32_t direction;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    clock_div = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    alignment = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    direction = ((pPmInt_t)p3)->val;

    timer_set_mode(timer_peripheral, clock_div, alignment, direction);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_clock_division():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t clock_div;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    clock_div = ((pPmInt_t)p1)->val;

    timer_set_clock_division(timer_peripheral, clock_div);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_preload():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_enable_preload(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_preload():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_disable_preload(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_alignment():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t alignment;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    alignment = ((pPmInt_t)p1)->val;

    timer_set_alignment(timer_peripheral, alignment);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_direction_up():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_direction_up(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_direction_down():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_direction_down(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_one_shot_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_one_shot_mode(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_continuous_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_continuous_mode(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_update_on_any():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_update_on_any(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_update_on_overflow():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_update_on_overflow(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_update_event():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_enable_update_event(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_update_event():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_disable_update_event(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_counter():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_enable_counter(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_counter():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_disable_counter(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_output_idle_state():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t outputs;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    outputs = ((pPmInt_t)p1)->val;

    timer_set_output_idle_state(timer_peripheral, outputs);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_reset_output_idle_state():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t outputs;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    outputs = ((pPmInt_t)p1)->val;

    timer_reset_output_idle_state(timer_peripheral, outputs);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_ti1_ch123_xor():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_set_ti1_ch123_xor(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_ti1_ch1():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    timer_set_ti1_ch1(timer_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_master_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t mode;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    mode = ((pPmInt_t)p1)->val;

    timer_set_master_mode(timer_peripheral, mode);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

 
    
def timer_set_prescaler():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t value;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    value = ((pPmInt_t)p1)->val;

    timer_set_prescaler(timer_peripheral, value);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_repetition_counter():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t value;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    value = ((pPmInt_t)p1)->val;

    timer_set_repetition_counter(timer_peripheral, value);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_period():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t period;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    period = ((pPmInt_t)p1)->val;

    timer_set_period(timer_peripheral, period);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_oc_clear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_enable_oc_clear(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_oc_clear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_disable_oc_clear(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_oc_fast_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_set_oc_fast_mode(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_oc_slow_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_set_oc_slow_mode(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_oc_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    uint32_t timer_peripheral;
    int oc_id;
    int oc_mode;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_mode = ((pPmInt_t)p2)->val;

    timer_set_oc_mode(timer_peripheral, oc_id, oc_mode);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_oc_preload():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_enable_oc_preload(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_oc_preload():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_disable_oc_preload(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_oc_polarity_high():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_set_oc_polarity_high(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_oc_polarity_low():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_set_oc_polarity_low(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_enable_oc_output():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_enable_oc_output(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_disable_oc_output():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    int oc_id;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    timer_disable_oc_output(timer_peripheral, oc_id);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_set_oc_value():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    uint32_t timer_peripheral;
    int oc_id;
    uint32_t value;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    oc_id = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    value = ((pPmInt_t)p2)->val;

    timer_set_oc_value(timer_peripheral, oc_id, value);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_generate_event():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t event;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    event = ((pPmInt_t)p1)->val;

    timer_generate_event(timer_peripheral, event);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def timer_get_counter():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t timer_peripheral;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    cret = timer_get_counter(timer_peripheral);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def timer_set_counter():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t count;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    count = ((pPmInt_t)p1)->val;

    timer_set_counter(timer_peripheral, count);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass


def timer_set_option():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t timer_peripheral;
    uint32_t option;

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

    timer_peripheral = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    option = ((pPmInt_t)p1)->val;

    timer_set_option(timer_peripheral, option);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
    
