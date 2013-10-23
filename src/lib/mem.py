# lib/mem.py
#
# Provides functionality to view and modify the running heap.
#
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

def heap_size():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t psize;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the heap size */
    retval = int_new(PM_HEAP_SIZE, &psize);
    PM_RETURN_IF_ERROR(retval);
    
    NATIVE_SET_TOS((pPmObj_t) psize);
    return retval;
    """
    pass

def heap_avail():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t pavail;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the heap available */
    retval = int_new(heap_getAvail(), &pavail);
    PM_RETURN_IF_ERROR(retval);
    
    NATIVE_SET_TOS((pPmObj_t) pavail);
    return retval;
    """
    pass

def heap_base():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t pbase;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the heap available */
    retval = int_new((uint32_t)heap_baseAddr(), &pbase);
    PM_RETURN_IF_ERROR(retval);
    
    NATIVE_SET_TOS((pPmObj_t) pbase);
    return retval;
    """
    pass

def heap_verify():
    """__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t pbool;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 0)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    /* Get the heap available */
    retval = heap_verify(&pbool);
    PM_RETURN_IF_ERROR(retval);
    
    NATIVE_SET_TOS(pbool);
    return retval;
    """
    pass

def inspect(addr, length=4, format=True):
    return _inspect(addr, length, format)

def _inspect(addr, length, format):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t     paddr;
    pPmInt_t     plen;
    pPmBoolean_t pfmt;
    uint8_t     *pstart;
    uint8_t     *pend;
    uint8_t     *pmem;
    uint8_t      i;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 3)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    paddr = (pPmInt_t) NATIVE_GET_LOCAL(0);
    plen  = (pPmInt_t) NATIVE_GET_LOCAL(1);
    pfmt  = (pPmBoolean_t) NATIVE_GET_LOCAL(2);

    if (OBJ_GET_TYPE(paddr) != OBJ_TYPE_INT)
    {
       PM_RAISE_WITH_OBJ(retval, PM_RET_EX_TYPE, (pPmObj_t) paddr);
       return retval;
    }
    if (OBJ_GET_TYPE(plen) != OBJ_TYPE_INT)
    {
       PM_RAISE_WITH_OBJ(retval, PM_RET_EX_TYPE, (pPmObj_t) plen);
       return retval;
    }
    if (OBJ_GET_TYPE(pfmt) != OBJ_TYPE_BOL)
    {
       PM_RAISE_WITH_OBJ(retval, PM_RET_EX_TYPE, (pPmObj_t) pfmt);
       return retval;
    }

    if (pfmt->val)
    {
       pstart = (uint8_t *)paddr->val;
       pend   = pstart + plen->val;
       pmem   = (uint8_t *) (((uint32_t) pstart) & 0xfffffff0);
       
       while (pmem < pend)
       {
          lib_printf("%10p:", pmem);
          for (i=0; i<16; i++)
          {
             if ((pmem < pstart) || (pmem >= pend))
             {
                lib_printf(" __");
             }
             else
             {
                lib_printf(" %02x", *pmem);
             }
             pmem++;
          }
          lib_printf("\n");
       }
    }
    else
    {
       pstart = (uint8_t *)paddr->val;
       pend   = pstart + plen->val;
       pmem   = pstart;

       while (pmem < pend)
       {
          lib_printf("%02X", *pmem);
          pmem++;
       }
    }

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass

def get_object(addr):
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmInt_t     paddr;
    uint32_t     size;
    uint8_t     *pstart;
    uint8_t     *pend;
    uint8_t     *pmem;

    /* If wrong number of args, raise TypeError */
    if (NATIVE_GET_NUM_ARGS() != 1)
    {
        PM_RAISE(retval, PM_RET_EX_TYPE);
        return retval;
    }

    paddr = (pPmInt_t) NATIVE_GET_LOCAL(0);

    if (OBJ_GET_TYPE(paddr) != OBJ_TYPE_INT)
    {
       PM_RAISE_WITH_OBJ(retval, PM_RET_EX_TYPE, (pPmObj_t) paddr);
       return retval;
    }

    pstart = (uint8_t *)paddr->val;
    size = OBJ_GET_SIZE(pstart);
    pend = pstart + size;
    pmem   = pstart;

    while (pmem < pend)
    {
       lib_printf("%02X", *pmem);
       pmem++;
    }

    NATIVE_SET_TOS(PM_NONE);
    return retval;
    """
    pass

def peek():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0;
    uint32_t *addr;

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

    addr = (uint32_t *) (((pPmInt_t)p0)->val);

    cret = *addr;

    int_new(cret, &pret);
    NATIVE_SET_TOS((pPmObj_t) pret);

    return retval;
    '''
    pass

    
def poke():
    r'''__NATIVE__
    PmReturn_t retval = PM_RET_OK;
    pPmObj_t p0, p1;
    uint32_t *addr;
    uint32_t val;

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

    addr = (uint32_t *) (((pPmInt_t)p0)->val);

    p1 = NATIVE_GET_LOCAL(1);

    /* If arg is not an int, raise TypeError */
    if (OBJ_GET_TYPE(p1) != OBJ_TYPE_INT)
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "expected int");
        return retval;
    }

    val = ((pPmInt_t)p1)->val;

    *addr = val;

    NATIVE_SET_TOS(PM_NONE);

    return retval;
    '''
    pass

