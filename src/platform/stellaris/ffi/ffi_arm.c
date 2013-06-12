/* -----------------------------------------------------------------------
   ffi.c - Copyright (c) 2011 Plausible Labs Cooperative, Inc.
           Copyright (c) 2011 Anthony Green
       Copyright (c) 2011 Free Software Foundation
           Copyright (c) 1998, 2008, 2011  Red Hat, Inc.
       
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

#include <ffi.h>
#include <ffi_common.h>
#include <stdlib.h>

/* ffi_prep_args is called by the assembly routine once stack space
   has been allocated for the function's arguments
   
*/
int ffi_prep_args(char *stack, extended_cif *ecif, float *vfp_space)
{
  register unsigned int i;
  register void **p_argv;
  register char *argp;
  register ffi_type **p_arg;

  argp = stack;

  if ( ecif->cif->flags == FFI_TYPE_STRUCT ) {
    *(void **) argp = ecif->rvalue;
    argp += 4;
  }

  p_argv = ecif->avalue;

  for (i = ecif->cif->nargs, p_arg = ecif->cif->arg_types;
       (i != 0);
       i--, p_arg++)
    {
      size_t z;

      /* Align if necessary */
      if (((*p_arg)->alignment - 1) & (unsigned) argp) {
    argp = (char *) ALIGN(argp, (*p_arg)->alignment);
      }

      if ((*p_arg)->type == FFI_TYPE_STRUCT)
    argp = (char *) ALIGN(argp, 4);

      z = (*p_arg)->size;
      if (z < sizeof(int))
        {
          z = sizeof(int);
          switch ((*p_arg)->type)
        {
        case FFI_TYPE_SINT8:
          *(signed int *) argp = (signed int)*(SINT8 *)(* p_argv);
          break;
          
        case FFI_TYPE_UINT8:
          *(unsigned int *) argp = (unsigned int)*(UINT8 *)(* p_argv);
          break;
          
        case FFI_TYPE_SINT16:
          *(signed int *) argp = (signed int)*(SINT16 *)(* p_argv);
          break;
          
        case FFI_TYPE_UINT16:
          *(unsigned int *) argp = (unsigned int)*(UINT16 *)(* p_argv);
          break;

        default:
          FFI_ASSERT(0);
        }
        }
      else if (z == sizeof(int))
        {
          *(unsigned int *) argp = (unsigned int)*(UINT32 *)(* p_argv);
        }
      else
        {
          memcpy(argp, *p_argv, z);
        }
      p_argv++;
      argp += z;
    }

  /* Indicate the VFP registers used. */
  return ecif->cif->vfp_used;
}

/* Perform machine dependent cif processing */
ffi_status ffi_prep_cif_machdep(ffi_cif *cif)
{

  /* Set the return type flag */
  switch (cif->rtype->type)
    {
    case FFI_TYPE_VOID:
    case FFI_TYPE_FLOAT:
    case FFI_TYPE_DOUBLE:
      cif->flags = (unsigned) cif->rtype->type;
      break;

    case FFI_TYPE_SINT64:
    case FFI_TYPE_UINT64:
      cif->flags = (unsigned) FFI_TYPE_SINT64;
      break;

    default:
      cif->flags = FFI_TYPE_INT;
      break;
    }

  return FFI_OK;
}

/* Prototypes for assembly functions, in sysv.S */
extern void ffi_call_EABI (void (*fn)(void), extended_cif *, unsigned, unsigned, unsigned *);

void ffi_call(ffi_cif *cif, void (*fn)(void), void *rvalue, void **avalue)
{
  extended_cif ecif;

  ecif.cif = cif;
  ecif.avalue = avalue;

  // on ARM, we always pop off four elements from the stack,
  // so lower bound it by that much
  cif->bytes = (4*(cif->nargs));
  if (cif->bytes <= 16) {
      cif->bytes = 16;
  }
  
  switch (cif->abi) 
    {
    case FFI_EABI:
      ffi_call_EABI (fn, &ecif, cif->bytes, cif->flags, rvalue);
      break;

    default:
      FFI_ASSERT(0);
      break;
    }
}

