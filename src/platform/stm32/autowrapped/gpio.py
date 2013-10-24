# autowrapped header for stm32
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "gpio.h"

'''


GPIO0 = 1
GPIO1 = 2
GPIO2 = 4
GPIO3 = 8
GPIO4 = 16
GPIO5 = 32
GPIO6 = 64
GPIO7 = 128
GPIO8 = 256
GPIO9 = 512
GPIO10 = 1024
GPIO11 = 2048
GPIO12 = 4096
GPIO13 = 8192
GPIO14 = 16384
GPIO15 = 32768
GPIO_ALL = 65535
GPIOA = 1073872896
GPIOB = 1073873920
GPIOC = 1073874944
GPIOD = 1073875968
GPIOE = 1073876992
GPIOF = 1073878016
GPIO_MODE_INPUT = 0
GPIO_MODE_OUTPUT = 1
GPIO_MODE_AF = 2
GPIO_MODE_ANALOG = 3
GPIO_OTYPE_PP = 0
GPIO_OTYPE_OD = 1
GPIO_OSPEED_2MHZ = 0
GPIO_OSPEED_25MHZ = 1
GPIO_OSPEED_50MHZ = 2
GPIO_OSPEED_100MHZ = 3
GPIO_PUPD_NONE = 0
GPIO_PUPD_PULLUP = 1
GPIO_PUPD_PULLDOWN = 2
GPIO_LCKK = 65536
GPIO_AF0 = 0
GPIO_AF1 = 1
GPIO_AF2 = 2
GPIO_AF3 = 3
GPIO_AF4 = 4
GPIO_AF5 = 5
GPIO_AF6 = 6
GPIO_AF7 = 7
GPIO_AF8 = 8
GPIO_AF9 = 9
GPIO_AF10 = 10
GPIO_AF11 = 11
GPIO_AF12 = 12
GPIO_AF13 = 13
GPIO_AF14 = 14
GPIO_AF15 = 15
GPIOG = 1073879040
GPIOH = 1073880064
GPIOI = 1073881088
def gpio_set():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t gpioport;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p1)->val;

    gpio_set(gpioport, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_clear():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t gpioport;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p1)->val;

    gpio_clear(gpioport, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_get():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t gpioport;
    uint16_t gpios;

    pPmInt_t pret;
    uint16_t cret;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p1)->val;

    cret = gpio_get(gpioport, gpios);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def gpio_toggle():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t gpioport;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p1)->val;

    gpio_toggle(gpioport, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_port_read():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t gpioport;

    pPmInt_t pret;
    uint16_t cret;

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

    gpioport = ((pPmInt_t)p0)->val;

    cret = gpio_port_read(gpioport);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def gpio_port_write():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t gpioport;
    uint16_t data;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    gpio_port_write(gpioport, data);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_port_config_lock():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t gpioport;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p1)->val;

    gpio_port_config_lock(gpioport, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_mode_setup():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    uint32_t gpioport;
    uint8_t mode;
    uint8_t pull_up_down;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    mode = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    pull_up_down = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p3)->val;

    gpio_mode_setup(gpioport, mode, pull_up_down, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_set_output_options():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3;
    uint32_t gpioport;
    uint8_t otype;
    uint8_t speed;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    otype = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    speed = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p3)->val;

    gpio_set_output_options(gpioport, otype, speed, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def gpio_set_af():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2;
    uint32_t gpioport;
    uint8_t alt_func_num;
    uint16_t gpios;

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

    gpioport = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    alt_func_num = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    gpios = ((pPmInt_t)p2)->val;

    gpio_set_af(gpioport, alt_func_num, gpios);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
