/* platform/stm32/stm32.h
 *
 * Private headers used by the platform/ module but NOT called by the VM.
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

PmReturn_t plat_preinit(void);
void       plat_timer_start(void);
void       plat_timer_stop(void);
void       plat_cts(int value);
void       plat_profiler_tick(void);
void       panic(int blinks);

