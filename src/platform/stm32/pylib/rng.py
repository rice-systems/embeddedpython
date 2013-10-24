# platform/stm32/pylib/rng.py
#
# Bit-banging interface to STM32 RNG.
#
# Copyright 2013 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import rcc
import mem

RNG_BASE = 1342572544

RNG_CR = 1342572544
RNG_SR = 1342572548
RNG_DR = 1342572552
RNG_CR_RNGEN = 4
RNG_CR_IE = 8
RNG_SR_DRDY = 1
RNG_SR_CECS = 2
RNG_SR_SECS = 4
RNG_SR_CEIS = 32
RNG_SR_SEIS = 64

def rcc_init():
    rcc.rcc_peripheral_enable_clock(rcc.RCC_AHB2_ENR, rcc.RCC_AHB2ENR_RNGEN)

def rand_int():
    # turn the RNG on
    rcc_init()
    mem.poke_bit(RNG_CR, RNG_CR_RNGEN, True)

    # wait for the data to be ready
    while not mem.peek_bit(RNG_SR, RNG_SR_DRDY):
        pass

    # read the data out
    out = mem.peek(RNG_DR)

    # turn the RNG back off
    mem.poke_bit(RNG_CR, RNG_CR_RNGEN, False)

    return out

