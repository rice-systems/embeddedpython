# autowrapped header for stm32
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "usart.h"

'''

USART1 = 1073811456
USART2 = 1073759232
USART3 = 1073760256
UART4 = 1073761280
UART5 = 1073762304

USART_FLOWCONTROL_NONE = 0
USART_SR_CTS = 512
USART_SR_LBD = 256
USART_SR_TXE = 128
USART_SR_TC = 64
USART_SR_RXNE = 32
USART_SR_IDLE = 16
USART_SR_ORE = 8
USART_SR_NE = 4
USART_SR_FE = 2
USART_SR_PE = 1
USART_DR_MASK = 511
USART_BRR_DIV_MANTISSA_MASK = 65520
USART_BRR_DIV_FRACTION_MASK = 15
USART_CR1_UE = 8192
USART_CR1_M = 4096
USART_CR1_WAKE = 2048
USART_CR1_PCE = 1024
USART_CR1_PS = 512
USART_CR1_PEIE = 256
USART_CR1_TXEIE = 128
USART_CR1_TCIE = 64
USART_CR1_RXNEIE = 32
USART_CR1_IDLEIE = 16
USART_CR1_TE = 8
USART_CR1_RE = 4
USART_CR1_RWU = 2
USART_CR1_SBK = 1
USART_CR2_LINEN = 16384
USART_CR2_STOPBITS_1 = 0
USART_CR2_STOPBITS_0_5 = 4096
USART_CR2_STOPBITS_2 = 8192
USART_CR2_STOPBITS_1_5 = 12288
USART_CR2_STOPBITS_MASK = 12288
USART_CR2_STOPBITS_SHIFT = 12
USART_CR2_CLKEN = 2048
USART_CR2_CPOL = 1024
USART_CR2_CPHA = 512
USART_CR2_LBCL = 256
USART_CR2_LBDIE = 64
USART_CR2_LBDL = 32
USART_CR2_ADD_MASK = 15
USART_CR3_CTSIE = 1024
USART_CR3_CTSE = 512
USART_CR3_RTSE = 256
USART_CR3_DMAT = 128
USART_CR3_DMAR = 64
USART_CR3_SCEN = 32
USART_CR3_NACK = 16
USART_CR3_HDSEL = 8
USART_CR3_IRLP = 4
USART_CR3_IREN = 2
USART_CR3_EIE = 1
USART_GTPR_GT_MASK = 65280
USART_GTPR_PSC_MASK = 255
USART6 = 1073812480
USART_CR1_OVER8 = 32768
USART_CR3_ONEBIT = 2048
USART_PARITY_NONE = 0
USART_MODE_RX = USART_CR1_RE
USART_MODE_TX = USART_CR1_TE 
USART_MODE_TX_RX = USART_CR1_RE | USART_CR1_TE 
USART_STOPBITS_1 = USART_CR2_STOPBITS_1

def usart_set_baudrate():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
    uint32_t baud;

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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    baud = ((pPmInt_t)p1)->val;

    usart_set_baudrate(usart, baud);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_set_databits():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
    uint32_t bits;

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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    bits = ((pPmInt_t)p1)->val;

    usart_set_databits(usart, bits);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_set_stopbits():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
    uint32_t stopbits;

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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    stopbits = ((pPmInt_t)p1)->val;

    usart_set_stopbits(usart, stopbits);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_set_parity():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
    uint32_t parity;

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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    parity = ((pPmInt_t)p1)->val;

    usart_set_parity(usart, parity);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_set_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    mode = ((pPmInt_t)p1)->val;

    usart_set_mode(usart, mode);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_set_flow_control():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
    uint32_t flowcontrol;

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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    flowcontrol = ((pPmInt_t)p1)->val;

    usart_set_flow_control(usart, flowcontrol);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_enable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_enable(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_disable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_disable(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_send():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    usart_send(usart, data);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_recv():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    cret = usart_recv(usart);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def usart_wait_send_ready():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_wait_send_ready(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_wait_recv_ready():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_wait_recv_ready(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_send_blocking():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    usart_send_blocking(usart, data);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_recv_blocking():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    cret = usart_recv_blocking(usart);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def usart_enable_rx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_enable_rx_dma(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_disable_rx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_disable_rx_dma(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_enable_tx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_enable_tx_dma(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_disable_tx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_disable_tx_dma(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_enable_rx_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_enable_rx_interrupt(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_disable_rx_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_disable_rx_interrupt(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_enable_tx_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_enable_tx_interrupt(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_disable_tx_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_disable_tx_interrupt(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_enable_error_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_enable_error_interrupt(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_disable_error_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t usart;

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

    usart = ((pPmInt_t)p0)->val;

    usart_disable_error_interrupt(usart);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def usart_get_flag():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    flag = ((pPmInt_t)p1)->val;

    cret = usart_get_flag(usart, flag);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
def usart_get_interrupt_source():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t usart;
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

    usart = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    flag = ((pPmInt_t)p1)->val;

    cret = usart_get_interrupt_source(usart, flag);

    if (cret == true) {
        NATIVE_SET_TOS(PM_TRUE);
    } else {
        NATIVE_SET_TOS(PM_FALSE);
    }

    return retval;
    '''
    pass

    
