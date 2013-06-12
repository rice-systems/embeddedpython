
/* -----------------------------------------------------------------------
   eabi.S - Copyright (c) 1998, 2008, 2011 Red Hat, Inc.
	    Copyright (c) 2011 Plausible Labs Cooperative, Inc.
	    Copyright (c) 2011 Thomas W. Barr, Rice University
   
   ARM Foreign Function Interface 

   Permission is hereby granted, free of charge, to any person obtaining
   a copy of this software and associated documentation files (the
   ``Software''), to deal in the Software without restriction, including
   without limitation the rights to use, copy, modify, merge, publish,
   distribute, sublicense, and/or sell copies of the Software, and to
   permit persons to whom the Software is furnished to do so, subject to
   the following conditions:

   The above copyright notice and this permission notice shall be included
   in all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED ``AS IS'', WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
   NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
   HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
   DEALINGS IN THE SOFTWARE.
   ----------------------------------------------------------------------- */

.macro ARM_FUNC_START name
 .text
 .align 0
 .cpu cortex-m3 
 .globl \name; .type \name,%function; \name:
 .fnstart
.endm

 @ r0: fn
 @ r1: &ecif
 @ r2: cif->bytes
 @ r3: cif->flags
 @ sp+0: ecif.rvalue

ARM_FUNC_START ffi_call_EABI
 @ Save registers
 
 push {r4, r5, r6, r7, lr}
 .save {r4, r5, r6, r7, lr}

 @ save the stack pointer and cif->flags for later
 mov r7, sp
 mov r5, r3

 @ Make room for all of the new args.
 @ r2 is cif->bytes
 mov r4, sp
 sub r4, r4, r2
 mov sp, r4

 @ save r6 for the function pointer
 mov r6, r0

 @ Place all of the ffi_prep_args in position
 mov r0, sp
 @ r1 already set

 @ Call ffi_prep_args(stack, &ecif)
 bl ffi_prep_args

 @ move first 4 parameters in registers as placed by ffi_prep_args
 pop {r0, r1, r2, r3}

 @ jump to fn
 blx r6

 @ restore the stack to what we had earlier
 mov sp, r7
 
 @ Reuse r4 with the pointer to storage for the return value
 ldr r4, [sp, #20]

@ If the return value pointer is NULL, assume no return value.
 cmp r4, #0
 beq .Lepilogue

 @ return INT
 @ if (r3 == 1) or (r3 == 2)
 cmp r5, #1
 beq returnint
 cmp r5, #2
 beq returnint
 b .Lepilogue

returnint:
 str r0, [r4]

.Lepilogue:
 pop {r4, r5, r6, r7, pc}

