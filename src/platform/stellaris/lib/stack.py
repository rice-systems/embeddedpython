"""__NATIVE__
#include "stellaris.h"
"""

import sys

RAM_TOP = 0x20000000
RAM_QUANT = 96*1024

def info():
    raw_info = _info()
    adjusted_info = [b-RAM_TOP for b in raw_info]

    (end, sp, first_painted, last_painted) = adjusted_info
    (heap_used, heap_size) = sys.heap()

    data_and_bss = end - heap_size
    print "RAM usage (in bytes):"
    print "----------------------------------------"
    print "         total RAM (assumed): %d" % RAM_QUANT
    print "            Python heap size: %d" % heap_size
    print " data+bss (less Python heap): %d" % (end - heap_size)
    print "                     C stack: %d" % (RAM_QUANT - last_painted)
    print "     bytes of RAM never used: %d" % (last_painted - first_painted)
    print "----------------------------------------"

    if (first_painted) == (end + 1):
        print "(no C heap touched)"
    else:
        print "***C heap NOT intact!!"

def _info():
    r"""__NATIVE__
    PmReturn_t retval = PM_RET_OK;

    extern uint8_t __end;
    uint8_t *sp;
    uint8_t *end;
    uint8_t *first_untouched = NULL;
    uint8_t *last_untouched = NULL;
    uint8_t *c;

    pPmInt_t pi;
    pPmTuple_t pt;

    end = &__end;
    asm("mov %[result], sp" : [result] "=r" (sp) : );

    c = end;
    while (c < sp) {
        if (*c == STACK_COLOR) {
            if (!first_untouched) {
                first_untouched = c;
            }
        } else {
            if (first_untouched) {
                last_untouched = c;
                break;
            }
        }
        c++;
    }

    retval = tuple_new(4, &pt);
    PM_RETURN_IF_ERROR(retval);

    retval = int_new((int) end, &pi);
    PM_RETURN_IF_ERROR(retval);
    pt->items[0] = (pPmObj_t) pi;
    
    retval = int_new((int) sp, &pi);
    PM_RETURN_IF_ERROR(retval);
    pt->items[1] = (pPmObj_t) pi;

    retval = int_new((int) first_untouched, &pi);
    PM_RETURN_IF_ERROR(retval);
    pt->items[2] = (pPmObj_t) pi;

    retval = int_new((int) last_untouched, &pi);
    PM_RETURN_IF_ERROR(retval);
    pt->items[3] = (pPmObj_t) pi;

    NATIVE_SET_TOS(pt);
    return retval;
    """
    pass 
