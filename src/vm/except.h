/* vm/except.h
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

void except_fatal(char *msg);
pPmFrame_t except_getFrameAtDepth(uint16_t depth);
uint16_t except_getStackDepth(void);
void except_printTrace(void);
void except_reportError(PmReturn_t result);
