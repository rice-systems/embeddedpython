# lib/ipm.py
#
# Provides the interactive prompt facility.
#
# This file is Copyright 2007, 2009 Dean Hall.
# Copyright 2011 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import sys

def _getImg():
    """__NATIVE__
    PmReturn_t retval;
    uint32_t od;
    uint16_t imgSize;
    uint8_t *pchunk;
    uint8_t hexbyte[2];
    uint8_t command;
    uint16_t i;
    pPmObj_t pco;

    /* Get the image type */
    do {
        retval = plat_getByte(&command);
        PM_RETURN_IF_ERROR(retval);
    } while (command == 'i'); /* spin if we see the code to start IPM */

    /* Quit if a code image command was not received */
    if (command != 'c')
    {
        PM_RAISE(retval, PM_RET_EX_STOP);
        return retval;
    }

    /* Get the image type */
    retval = plat_getByte(&hexbyte[0]);
    PM_RETURN_IF_ERROR(retval);
    retval = plat_getByte(&hexbyte[1]);
    PM_RETURN_IF_ERROR(retval);

    od = xtod_byte((char *) hexbyte);

    /* Quit if a packed code object was not received */
    if (od != OBJ_TYPE_PCO)
    {
        PM_RAISE(retval, PM_RET_EX_STOP);
        return retval;
    }

    /* Get the remainder of the object descriptor */
    retval = plat_getByte(&hexbyte[0]);
    PM_RETURN_IF_ERROR(retval);
    retval = plat_getByte(&hexbyte[1]);
    PM_RETURN_IF_ERROR(retval);
    od |= xtod_byte((char *) hexbyte) << 8;
    
    retval = plat_getByte(&hexbyte[0]);
    PM_RETURN_IF_ERROR(retval);
    retval = plat_getByte(&hexbyte[1]);
    PM_RETURN_IF_ERROR(retval);
    od |= xtod_byte((char *) hexbyte) << 16;

    retval = plat_getByte(&hexbyte[0]);
    PM_RETURN_IF_ERROR(retval);
    retval = plat_getByte(&hexbyte[1]);
    PM_RETURN_IF_ERROR(retval);
    od |= xtod_byte((char *) hexbyte) << 24;

    imgSize = OBJ_GET_SIZE((pPmObj_t)&od);

    /* Get space for CodeImgObj */
    retval = heap_getChunk(imgSize, &pchunk);
    PM_RETURN_IF_ERROR(retval);
    pco = (pPmObj_t)pchunk;
    OBJ_SET_TYPE(pco, OBJ_TYPE_PCO);

    /* Get the remaining bytes in the image */
    for(i=4; i < imgSize; i++)
    {
        retval = plat_getByte(&hexbyte[0]);
        PM_RETURN_IF_ERROR(retval);
        retval = plat_getByte(&hexbyte[1]);
        PM_RETURN_IF_ERROR(retval);
        pchunk[i] = xtod_byte((char *) hexbyte);
    }

    /* Return the image */
    NATIVE_SET_TOS(pco);
    return retval;
    """
    pass


##
# Runs the target device-side interactive session.
#
def ipm(g={}):
    while 1:
        # Wait for a code image, make a code object from it
        # and evaluate the code object.
        # #180: One-liner turned into 3 so that objects get bound to roots
        sys.gcRun()
        co = copy(_getImg())
        rv = eval(co, g)

        # Send a byte to indicate completion of evaluation
        sys.putb(0x04)

# :mode=c:
