# autowrapped header for stm32
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "rcc.h"
#include "rcc_intermd_func.h"

'''

RCC_AHB1_ENR = 0
RCC_AHB2_ENR = 1
RCC_AHB3_ENR = 2
RCC_APB1_ENR = 3
RCC_APB2_ENR = 4
RCC_AHB1_RSTR = 0
RCC_AHB2_RSTR = 1
RCC_AHB3_RSTR = 2
RCC_APB1_RSTR = 3
RCC_APB2_RSTR = 4
CLOCK_8MHZ_3V3 = 0
CLOCK_12MHZ_3V3 = 1
CLOCK_16MHZ_3V3 = 2
CLOCK_SCALE_NUM = 3
RCC_AHB1RSTR_OTGHSRST = 536870912
RCC_AHB1RSTR_IOPIRST = 256
RCC_AHB1RSTR_IOPHRST = 128
RCC_AHB1RSTR_IOPGRST = 64
RCC_AHB1RSTR_IOPFRST = 32
RCC_AHB1RSTR_IOPERST = 16
RCC_AHB1RSTR_IOPDRST = 8
RCC_AHB1RSTR_IOPCRST = 4
RCC_AHB1RSTR_IOPBRST = 2
RCC_AHB1RSTR_IOPARST = 1
RCC_AHB2RSTR_OTGFSRST = 128
RCC_AHB2RSTR_RNGRST = 64
RCC_AHB2RSTR_HASHRST = 32
RCC_AHB2RSTR_CRYPRST = 16
RCC_AHB2RSTR_DCMIRST = 1
RCC_AHB3RSTR_FSMCRST = 1
RCC_APB1RSTR_DACRST = 536870912
RCC_APB1RSTR_PWRRST = 268435456
RCC_APB1RSTR_CAN2RST = 67108864
RCC_APB1RSTR_CAN1RST = 33554432
RCC_APB1RSTR_I2C3RST = 8388608
RCC_APB1RSTR_I2C2RST = 4194304
RCC_APB1RSTR_I2C1RST = 2097152
RCC_APB1RSTR_UART5RST = 1048576
RCC_APB1RSTR_UART4RST = 524288
RCC_APB1RSTR_USART3RST = 262144
RCC_APB1RSTR_USART2RST = 131072
RCC_APB1RSTR_SPI3RST = 32768
RCC_APB1RSTR_SPI2RST = 16384
RCC_APB1RSTR_TIM14RST = 256
RCC_APB1RSTR_TIM13RST = 128
RCC_APB1RSTR_TIM12RST = 64
RCC_APB1RSTR_TIM7RST = 32
RCC_APB1RSTR_TIM6RST = 16
RCC_APB1RSTR_TIM5RST = 8
RCC_APB1RSTR_TIM4RST = 4
RCC_APB1RSTR_TIM3RST = 2
RCC_APB1RSTR_TIM2RST = 1
RCC_APB2RSTR_TIM11RST = 262144
RCC_APB2RSTR_TIM10RST = 131072
RCC_APB2RSTR_TIM9RST = 65536
RCC_APB2RSTR_SYSCFGRST = 16384
RCC_APB2RSTR_SPI1RST = 4096
RCC_APB2RSTR_SDIORST = 2048
RCC_APB2RSTR_ADCRST = 256
RCC_APB2RSTR_USART6RST = 32
RCC_APB2RSTR_USART1RST = 16
RCC_APB2RSTR_TIM8RST = 2
RCC_APB2RSTR_TIM1RST = 1
RCC_AHB1ENR_OTGHSULPIEN = 1073741824
RCC_AHB1ENR_OTGHSEN = 536870912
RCC_AHB1ENR_CRCEN = 4096
RCC_AHB1ENR_IOPIEN = 256
RCC_AHB1ENR_IOPHEN = 128
RCC_AHB1ENR_IOPGEN = 64
RCC_AHB1ENR_IOPFEN = 32
RCC_AHB1ENR_IOPEEN = 16
RCC_AHB1ENR_IOPDEN = 8
RCC_AHB1ENR_IOPCEN = 4
RCC_AHB1ENR_IOPBEN = 2
RCC_AHB1ENR_IOPAEN = 1
RCC_AHB2ENR_OTGFSEN = 128
RCC_AHB2ENR_RNGEN = 64
RCC_AHB2ENR_HASHEN = 32
RCC_AHB2ENR_CRYPEN = 16
RCC_AHB2ENR_DCMIEN = 1
RCC_AHB3ENR_FSMCEN = 1
RCC_APB1ENR_DACEN = 536870912
RCC_APB1ENR_PWREN = 268435456
RCC_APB1ENR_CAN2EN = 67108864
RCC_APB1ENR_CAN1EN = 33554432
RCC_APB1ENR_I2C3EN = 8388608
RCC_APB1ENR_I2C2EN = 4194304
RCC_APB1ENR_I2C1EN = 2097152
RCC_APB1ENR_UART5EN = 1048576
RCC_APB1ENR_UART4EN = 524288
RCC_APB1ENR_USART3EN = 262144
RCC_APB1ENR_USART2EN = 131072
RCC_APB1ENR_SPI3EN = 32768
RCC_APB1ENR_SPI2EN = 16384
RCC_APB1ENR_WWDGEN = 2048
RCC_APB1ENR_TIM14EN = 256
RCC_APB1ENR_TIM13EN = 128
RCC_APB1ENR_TIM12EN = 64
RCC_APB1ENR_TIM7EN = 32
RCC_APB1ENR_TIM6EN = 16
RCC_APB1ENR_TIM5EN = 8
RCC_APB1ENR_TIM4EN = 4
RCC_APB1ENR_TIM3EN = 2
RCC_APB1ENR_TIM2EN = 1
RCC_APB2ENR_TIM11EN = 262144
RCC_APB2ENR_TIM10EN = 131072
RCC_APB2ENR_TIM9EN = 65536
RCC_APB2ENR_SYSCFGEN = 16384
RCC_APB2ENR_SPI1EN = 4096
RCC_APB2ENR_SDIOEN = 2048
RCC_APB2ENR_ADC3EN = 1024
RCC_APB2ENR_ADC2EN = 512
RCC_APB2ENR_ADC1EN = 256
RCC_APB2ENR_USART6EN = 32
RCC_APB2ENR_USART1EN = 16
RCC_APB2ENR_TIM8EN = 2
RCC_APB2ENR_TIM1EN = 1

# WARNING: unable to parse declaration of function rcc_peripheral_enable_clock. skipped.
# WARNING: unable to parse declaration of function rcc_peripheral_disable_clock. skipped.
# WARNING: unable to parse declaration of function rcc_peripheral_reset. skipped.
# WARNING: unable to parse declaration of function rcc_peripheral_clear_reset. skipped.

def rcc_peripheral_enable_clock():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    int reg;
    uint32_t en;

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

    reg = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    en = ((pPmInt_t)p1)->val;

    rcc_peripheral_enable_clock_new(reg, en);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def rcc_peripheral_disable_clock():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    int reg;
    uint32_t en;

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

    reg = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    en = ((pPmInt_t)p1)->val;

    rcc_peripheral_disable_clock_new(reg, en);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def rcc_peripheral_reset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    int reg;
    uint32_t reset;

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

    reg = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    reset = ((pPmInt_t)p1)->val;

    rcc_peripheral_reset_new(reg, reset);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def rcc_peripheral_clear_reset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    int reg;
    uint32_t clear_reset;

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

    reg = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    clear_reset = ((pPmInt_t)p1)->val;

    rcc_peripheral_clear_reset_new(reg, clear_reset);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def rcc_clock_setup_hse_3v3():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    int clock;

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

    clock = ((pPmInt_t)p0)->val;

    rcc_clock_setup_hse_3v3_new(clock);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

def rcc_set_sysclk_source():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t clk;

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

    clk = ((pPmInt_t)p0)->val;

    rcc_set_sysclk_source(clk);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def rcc_system_clock_source():
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

    cret = rcc_system_clock_source();

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass


    
