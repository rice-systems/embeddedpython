# autowrapped header for stm32
# do NOT modify
# twb at edu dot rice

r'''__NATIVE__

#include "spi.h"

'''


SPI1 = 1073819648
SPI2 = 1073756160
SPI3 = 1073757184
SPI_CR1_BIDIMODE_2LINE_UNIDIR = 0
SPI_CR1_BIDIMODE_1LINE_BIDIR = 32768
SPI_CR1_BIDIMODE = 32768
SPI_CR1_BIDIOE = 16384
SPI_CR1_CRCEN = 8192
SPI_CR1_CRCNEXT = 4096
SPI_CR1_RXONLY = 1024
SPI_CR1_SSM = 512
SPI_CR1_SSI = 256
SPI_CR1_MSBFIRST = 0
SPI_CR1_LSBFIRST = 128
SPI_CR1_SPE = 64
SPI_CR1_BAUDRATE_FPCLK_DIV_2 = 0
SPI_CR1_BAUDRATE_FPCLK_DIV_4 = 8
SPI_CR1_BAUDRATE_FPCLK_DIV_8 = 16
SPI_CR1_BAUDRATE_FPCLK_DIV_16 = 24
SPI_CR1_BAUDRATE_FPCLK_DIV_32 = 32
SPI_CR1_BAUDRATE_FPCLK_DIV_64 = 40
SPI_CR1_BAUDRATE_FPCLK_DIV_128 = 48
SPI_CR1_BAUDRATE_FPCLK_DIV_256 = 56
SPI_CR1_BR_FPCLK_DIV_2 = 0
SPI_CR1_BR_FPCLK_DIV_4 = 1
SPI_CR1_BR_FPCLK_DIV_8 = 2
SPI_CR1_BR_FPCLK_DIV_16 = 3
SPI_CR1_BR_FPCLK_DIV_32 = 4
SPI_CR1_BR_FPCLK_DIV_64 = 5
SPI_CR1_BR_FPCLK_DIV_128 = 6
SPI_CR1_BR_FPCLK_DIV_256 = 7
SPI_CR1_MSTR = 4
SPI_CR1_CPOL_CLK_TO_0_WHEN_IDLE = 0
SPI_CR1_CPOL_CLK_TO_1_WHEN_IDLE = 2
SPI_CR1_CPOL = 2
SPI_CR1_CPHA_CLK_TRANSITION_1 = 0
SPI_CR1_CPHA_CLK_TRANSITION_2 = 1
SPI_CR1_CPHA = 1
SPI_CR2_TXEIE = 128
SPI_CR2_RXNEIE = 64
SPI_CR2_ERRIE = 32
SPI_CR2_SSOE = 4
SPI_CR2_TXDMAEN = 2
SPI_CR2_RXDMAEN = 1
SPI_SR_BSY = 128
SPI_SR_OVR = 64
SPI_SR_MODF = 32
SPI_SR_CRCERR = 16
SPI_SR_UDR = 8
SPI_SR_CHSIDE = 4
SPI_SR_TXE = 2
SPI_SR_RXNE = 1
SPI_I2SCFGR_I2SMOD = 2048
SPI_I2SCFGR_I2SE = 1024
SPI_I2SCFGR_I2SCFG_LSB = 8
SPI_I2SCFGR_I2SCFG_SLAVE_TRANSMIT = 0
SPI_I2SCFGR_I2SCFG_SLAVE_RECEIVE = 1
SPI_I2SCFGR_I2SCFG_MASTER_TRANSMIT = 2
SPI_I2SCFGR_I2SCFG_MASTER_RECEIVE = 3
SPI_I2SCFGR_PCMSYNC = 128
SPI_I2SCFGR_I2SSTD_LSB = 4
SPI_I2SCFGR_I2SSTD_I2S_PHILLIPS = 0
SPI_I2SCFGR_I2SSTD_MSB_JUSTIFIED = 1
SPI_I2SCFGR_I2SSTD_LSB_JUSTIFIED = 2
SPI_I2SCFGR_I2SSTD_PCM = 3
SPI_I2SCFGR_CKPOL = 8
SPI_I2SCFGR_DATLEN_LSB = 1
SPI_I2SCFGR_DATLEN_16BIT = 0
SPI_I2SCFGR_DATLEN_24BIT = 1
SPI_I2SCFGR_DATLEN_32BIT = 2
SPI_I2SCFGR_CHLEN = 1
SPI_I2SPR_MCKOE = 512
SPI_I2SPR_ODD = 256
SPI_CR1_DFF_8BIT = 0
SPI_CR1_DFF_16BIT = 2048
SPI_CR1_DFF = 2048
SPI_CR2_FRF = 16
SPI_CR2_FRF_MOTOROLA_MODE = 0
SPI_CR2_FRF_TI_MODE = 16
SPI_SR_TIFRFE = 256
def spi_reset():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi_peripheral;

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

    spi_peripheral = ((pPmInt_t)p0)->val;

    spi_reset(spi_peripheral);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_init_master():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1, p2, p3, p4, p5;
    uint32_t spi;
    uint32_t br;
    uint32_t cpol;
    uint32_t cpha;
    uint32_t dff;
    uint32_t lsbfirst;

    pPmInt_t pret;
    int cret;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 6)
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

    spi = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    br = ((pPmInt_t)p1)->val;

    p2 = NATIVE_GET_LOCAL(2);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p2) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    cpol = ((pPmInt_t)p2)->val;

    p3 = NATIVE_GET_LOCAL(3);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p3) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    cpha = ((pPmInt_t)p3)->val;

    p4 = NATIVE_GET_LOCAL(4);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p4) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    dff = ((pPmInt_t)p4)->val;

    p5 = NATIVE_GET_LOCAL(5);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p5) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    lsbfirst = ((pPmInt_t)p5)->val;

    cret = spi_init_master(spi, br, cpol, cpha, dff, lsbfirst);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def spi_enable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_clean_disable():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    cret = spi_clean_disable(spi);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def spi_write():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t spi;
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

    spi = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    spi_write(spi, data);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_send():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t spi;
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

    spi = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    spi_send(spi, data);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_read():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    cret = spi_read(spi);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def spi_xfer():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t spi;
    uint16_t data;

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

    spi = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    data = ((pPmInt_t)p1)->val;

    cret = spi_xfer(spi, data);

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def spi_set_bidirectional_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_bidirectional_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_unidirectional_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_unidirectional_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_bidirectional_receive_only_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_bidirectional_receive_only_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_bidirectional_transmit_only_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_bidirectional_transmit_only_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_crc():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_crc(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_crc():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_crc(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_next_tx_from_buffer():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_next_tx_from_buffer(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_next_tx_from_crc():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_next_tx_from_crc(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_dff_8bit():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_dff_8bit(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_dff_16bit():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_dff_16bit(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_full_duplex_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_full_duplex_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_receive_only_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_receive_only_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_software_slave_management():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_software_slave_management(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_software_slave_management():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_software_slave_management(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_nss_high():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_nss_high(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_nss_low():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_nss_low(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_send_lsb_first():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_send_lsb_first(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_send_msb_first():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_send_msb_first(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_baudrate_prescaler():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t spi;
    uint8_t baudrate;

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

    spi = ((pPmInt_t)p0)->val;

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    baudrate = ((pPmInt_t)p1)->val;

    spi_set_baudrate_prescaler(spi, baudrate);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_master_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_master_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_slave_mode():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_slave_mode(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_clock_polarity_1():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_clock_polarity_1(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_clock_polarity_0():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_clock_polarity_0(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_clock_phase_1():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_clock_phase_1(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_set_clock_phase_0():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_set_clock_phase_0(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_tx_buffer_empty_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_tx_buffer_empty_interrupt(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_tx_buffer_empty_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_tx_buffer_empty_interrupt(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_rx_buffer_not_empty_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_rx_buffer_not_empty_interrupt(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_rx_buffer_not_empty_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_rx_buffer_not_empty_interrupt(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_error_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_error_interrupt(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_error_interrupt():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_error_interrupt(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_ss_output():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_ss_output(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_ss_output():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_ss_output(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_tx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_tx_dma(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_tx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_tx_dma(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_enable_rx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_enable_rx_dma(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
def spi_disable_rx_dma():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t spi;

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

    spi = ((pPmInt_t)p0)->val;

    spi_disable_rx_dma(spi);

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

    
