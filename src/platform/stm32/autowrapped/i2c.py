# autowrapped header for stm32
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "i2c.h"

'''

I2C_CR1_SWRST = 32768
I2C_CR1_ALERT = 8192
I2C_CR1_PEC = 4096
I2C_CR1_POS = 2048
I2C_CR1_ACK = 1024
I2C_CR1_STOP = 512
I2C_CR1_START = 256
I2C_CR1_NOSTRETCH = 128
I2C_CR1_ENGC = 64
I2C_CR1_ENPEC = 32
I2C_CR1_ENARP = 16
I2C_CR1_SMBTYPE = 8
I2C_CR1_SMBUS = 2
I2C_CR1_PE = 1
I2C_CR2_LAST = 4096
I2C_CR2_DMAEN = 2048
I2C_CR2_ITBUFEN = 1024
I2C_CR2_ITEVTEN = 512
I2C_CR2_ITERREN = 256
I2C_CR2_FREQ_2MHZ = 2
I2C_CR2_FREQ_3MHZ = 3
I2C_CR2_FREQ_4MHZ = 4
I2C_CR2_FREQ_5MHZ = 5
I2C_CR2_FREQ_6MHZ = 6
I2C_CR2_FREQ_7MHZ = 7
I2C_CR2_FREQ_8MHZ = 8
I2C_CR2_FREQ_9MHZ = 9
I2C_CR2_FREQ_10MHZ = 10
I2C_CR2_FREQ_11MHZ = 11
I2C_CR2_FREQ_12MHZ = 12
I2C_CR2_FREQ_13MHZ = 13
I2C_CR2_FREQ_14MHZ = 14
I2C_CR2_FREQ_15MHZ = 15
I2C_CR2_FREQ_16MHZ = 16
I2C_CR2_FREQ_17MHZ = 17
I2C_CR2_FREQ_18MHZ = 18
I2C_CR2_FREQ_19MHZ = 19
I2C_CR2_FREQ_20MHZ = 20
I2C_CR2_FREQ_21MHZ = 21
I2C_CR2_FREQ_22MHZ = 22
I2C_CR2_FREQ_23MHZ = 23
I2C_CR2_FREQ_24MHZ = 24
I2C_CR2_FREQ_25MHZ = 25
I2C_CR2_FREQ_26MHZ = 26
I2C_CR2_FREQ_27MHZ = 27
I2C_CR2_FREQ_28MHZ = 28
I2C_CR2_FREQ_29MHZ = 29
I2C_CR2_FREQ_30MHZ = 30
I2C_CR2_FREQ_31MHZ = 31
I2C_CR2_FREQ_32MHZ = 32
I2C_CR2_FREQ_33MHZ = 33
I2C_CR2_FREQ_34MHZ = 34
I2C_CR2_FREQ_35MHZ = 35
I2C_CR2_FREQ_36MHZ = 36
I2C_CR2_FREQ_37MHZ = 37
I2C_CR2_FREQ_38MHZ = 38
I2C_CR2_FREQ_39MHZ = 39
I2C_CR2_FREQ_40MHZ = 40
I2C_CR2_FREQ_41MHZ = 41
I2C_CR2_FREQ_42MHZ = 42
I2C_OAR1_ADDMODE = 32768
I2C_OAR1_ADDMODE_7BIT = 0
I2C_OAR1_ADDMODE_10BIT = 1
I2C_OAR2_ENDUAL = 1
I2C_SR1_SMBALERT = 32768
I2C_SR1_TIMEOUT = 16384
I2C_SR1_PECERR = 4096
I2C_SR1_OVR = 2048
I2C_SR1_AF = 1024
I2C_SR1_ARLO = 512
I2C_SR1_BERR = 256
I2C_SR1_TxE = 128
I2C_SR1_RxNE = 64
I2C_SR1_STOPF = 16
I2C_SR1_ADD10 = 8
I2C_SR1_BTF = 4
I2C_SR1_ADDR = 2
I2C_SR1_SB = 1
I2C_SR2_DUALF = 128
I2C_SR2_SMBHOST = 64
I2C_SR2_SMBDEFAULT = 32
I2C_SR2_GENCALL = 16
I2C_SR2_TRA = 4
I2C_SR2_BUSY = 2
I2C_SR2_MSL = 1
I2C_CCR_FS = 32768
I2C_CCR_DUTY = 16384
I2C_CCR_DUTY_DIV2 = 0
I2C_CCR_DUTY_16_DIV_9 = 1
I2C_WRITE = 0
I2C_READ = 1

def i2c_reset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_reset(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_peripheral_enable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_peripheral_enable(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_peripheral_disable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_peripheral_disable(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_send_start():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_send_start(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_send_stop():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_send_stop(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_clear_stop():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_clear_stop(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_own_7bit_slave_address():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint8_t slave;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    slave = ((pPmInt_t)p1)->val;

    i2c_set_own_7bit_slave_address(i2c, slave);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_own_10bit_slave_address():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint16_t slave;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    slave = ((pPmInt_t)p1)->val;

    i2c_set_own_10bit_slave_address(i2c, slave);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_clock_frequency():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint8_t freq;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    freq = ((pPmInt_t)p1)->val;

    i2c_set_clock_frequency(i2c, freq);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_send_data():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint8_t data;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    i2c_send_data(i2c, data);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_fast_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_set_fast_mode(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_standard_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_set_standard_mode(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_ccr():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint16_t freq;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    freq = ((pPmInt_t)p1)->val;

    i2c_set_ccr(i2c, freq);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_trise():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint16_t trise;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    trise = ((pPmInt_t)p1)->val;

    i2c_set_trise(i2c, trise);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_send_7bit_address():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    uint32_t i2c;
    uint8_t slave;
    uint8_t readwrite;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    slave = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    readwrite = ((pPmInt_t)p2)->val;

    i2c_send_7bit_address(i2c, slave, readwrite);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_get_data():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

    pPmInt_t pret;
    uint8_t cret;

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

    i2c = ((pPmInt_t)p0)->val;

    cret = i2c_get_data(i2c);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def i2c_enable_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint32_t interrupt;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    interrupt = ((pPmInt_t)p1)->val;

    i2c_enable_interrupt(i2c, interrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_disable_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint32_t interrupt;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    interrupt = ((pPmInt_t)p1)->val;

    i2c_disable_interrupt(i2c, interrupt);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_enable_ack():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_enable_ack(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_disable_ack():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_disable_ack(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_nack_next():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_nack_next(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_nack_current():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_nack_current(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_dutycycle():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t i2c;
    uint32_t dutycycle;

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

    i2c = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    dutycycle = ((pPmInt_t)p1)->val;

    i2c_set_dutycycle(i2c, dutycycle);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_enable_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_enable_dma(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_disable_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_disable_dma(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_set_dma_last_transfer():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_set_dma_last_transfer(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def i2c_clear_dma_last_transfer():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t i2c;

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

    i2c = ((pPmInt_t)p0)->val;

    i2c_clear_dma_last_transfer(i2c);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
