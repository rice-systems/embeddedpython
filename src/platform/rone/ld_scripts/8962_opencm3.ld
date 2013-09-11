/*
 * This file is part of the libopencm3 project and has been modified for the 
 * Owl Embedded Python System.
 *
 * Copyright (C) 2009 Uwe Hermann <uwe@hermann-uwe.de>
 * Copyright (C) 2011 Stephen Caudle <scaudle@doceme.com>
 * Copyright 2012 Rice University <twb@rice.edu>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

/* Linker script for ST STM32F4DISCOVERY (STM32F407VG, 1024K flash, 128K RAM). */

/* Define memory regions. */
MEMORY
{
  ram (rwx) : ORIGIN = 0x20000000, LENGTH = 64K
  rom (rx) : ORIGIN = 0x00000000, LENGTH = 256K
  boot (rx) : ORIGIN = 0x01000000, LENGTH = 0x5f00
}

/* Include the common ld script. */
INCLUDE ld_scripts/libopencm3_lm3s.ld

