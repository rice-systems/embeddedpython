/* vm/int.c
 *
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#include "pm.h"
#include "limits.h"
#include "math.h"

// Maximum number of fractional digits to print
#define FRACDIGITS 6
// Multiplier to get FRACDIGITS as an integer (10^FRACDIGITS) 
#define FRACMULT 1000000

typedef void (*printfn)(void *pstate, uint16_t nchars, const char *pstr);
static int32_t lib_vprint(printfn printer, void *pstate,
                          const char *pformat, va_list vaargs);


/**
 * Write characters to the console.
 *
 * @param   pstate - current state of the "printer", not used for console
 * @param   nchars - number of characters to write
 * @param   pstr   - pointer to characters to write
 */
static void
console_write(void *pstate, uint16_t nchars, const char *pstr)
{
    while (nchars--)
    {
        plat_putByte(*pstr++);
    }
}

/**
 * Buffer to print to.
 */
typedef struct {
    char *pbuf;
    int   len;
} bufstate;

/**
 * Write characters to a buffer.
 *
 * @param   pstate - current state of the "printer", which is the output buffer
 * @param   nchars - number of characters to write
 * @param   pstr   - pointer to characters to write
 */
static void
buffer_write(void *pstate, uint16_t nchars, const char *pstr)
{
    bufstate *pb = (bufstate *) pstate;

    while (nchars--)
    {
        if (pb->len) 
        {
            *(pb->pbuf++) = *pstr++;
            pb->len--;
        }    
    }
}

/**
 * Print to the console
 *
 * @param   pformat - printf format string
 * @param   varargs - arguments to insert into format string
 * @return  number of characters printed
 */
int32_t
lib_printf(const char *pformat, ...)
{
    int retval;
    va_list arglist;
    va_start(arglist, pformat);
    retval = lib_vprint(console_write, C_NULL, pformat, arglist);
    va_end(arglist);
    return retval;
}                        

/**
 * Print to a string
 *
 * @param   pstr    - buffer to print to
 * @param   size    - size of buffer
 * @param   pformat - printf format string
 * @param   varargs - arguments to insert into format string
 * @return  number of characters printed
 */
int32_t
lib_snprintf(char *pstr, size_t size, const char *pformat, ...)
{
    int32_t retval;
    bufstate buffer;
    va_list arglist;
    va_start(arglist, pformat);
    buffer.pbuf = pstr;
    buffer.len = size;
    retval = lib_vprint(buffer_write, &buffer, pformat, arglist);
    va_end(arglist);

    if (retval == -1)
    {
        // Error
        return retval;
    }

    if (size)
    {
        // null terminate if size is at least 1
        if (((uint32_t) retval) < size)
        {
            pstr[retval] = '\0';
        }
        else
        {
            pstr[size-1] = '\0';
        }
    }
    return retval;
}

/**
 * Print integer number
 *
 * @param   printer  - printing function
 * @param   pstate   - current state of the "printer"
 * @param   number   - absolute value of integer number to print
 * @param   is_neg   - true if negative, false otherwise
 * @param   width    - width of field in which to print (0 for infinite)
 * @param   base     - base in which to print number
 * @param   charmap  - character map for numbers 0 to (base-1)
 * @param   zerofill - fill with zeros if true
 * @return  number of characters printed
 */
static int32_t
print_int(printfn printer, void *pstate,
          uint32_t number, bool is_neg, uint8_t width,
          uint8_t base, char *charmap, bool zerofill)
{
    uint32_t retval = 0;
    uint32_t val;
    uint32_t maxval = UINT_MAX / base;
    uint8_t  nchars = 1;
    int16_t  i;
    char     fillchar;
    char     buf[32]; // big enough for any number base 2

    if (is_neg)
    {
        // Space for the '-'
        nchars++;
    }

    // Determine number of digits in number
    for (val = base; val <= number; )
    {
        nchars++;
        if (val > maxval)
        {
            // Overflow
            break;
        }
        val *= base;
    }

    // Put negative sign first if zero filling
    if (zerofill && is_neg)
    {
        printer(pstate, 1, "-");
        retval++;
    }
        
    // Fill, if necessary
    fillchar = zerofill ? '0' : ' ';
    while (width > nchars)
    {
        printer(pstate, 1, &fillchar);
        retval++;
        width--;
    }

    // Put negative sign last if filling with spaces
    if (!zerofill && is_neg)
    {
        printer(pstate, 1, "-");
        retval++;
    }

    if (is_neg)
    {
        nchars--;
    }

    for (i = nchars - 1; i >= 0; i--)
    {
        buf[i] = charmap[(number % base)];
        number /= base;
    }

    printer(pstate, nchars, buf);
    retval += nchars;

    return retval;
}

#ifdef HAVE_FLOAT
/**
 * Print floating point number
 *
 * @param   printer - printing function
 * @param   pstate  - current state of the "printer"
 * @param   fnumber - floating point number to print
 * @return  number of characters printed
 */
static int32_t
print_flt(printfn printer, void *pstate, float fnumber)
{
    uint32_t retval = 0;
    uint32_t intpart, fracpart;
    uint8_t  digits;
    uint8_t  exp = 0;
    float    fremainder, ffrac;
    bool     is_neg = false;

    // Handle negative numbers
    if (fnumber < 0.0)
    {
        is_neg = true;
        fnumber = -fnumber;
    }

    // Handle infinite numbers
    if (!isfinite(fnumber))
    {
        if (is_neg)
        {
            printer(pstate, 1, "-");
            retval += 1;
        }
        printer(pstate, 3, "inf");
        retval += 3;
        return retval;
    }
                 
    // Handle large floating point numbers
    if (fnumber > UINT_MAX)
    {
        while (fnumber >= 10.0)
        {
            fnumber /= 10.0;
            exp++;
        }
    }
   
    // Separate integer part and remainder
    intpart = (unsigned long) fnumber;
    fremainder = fnumber - intpart;
    ffrac = FRACMULT * fremainder;
    fracpart = (unsigned long) ffrac;

    // Round
    if ((ffrac - fracpart) >= 0.5)
    {
        fracpart++;
    }
    if (fracpart >= FRACMULT)
    {
        intpart++;
        fracpart = 0;
    }

    // Print integer part
    retval += print_int(printer, pstate, intpart, is_neg, 0, 10, "0123456789", false);

    // Print decimal point
    if (FRACDIGITS > 0)
    {
        printer(pstate, 1, ".");
        retval++;
    }

    // Remove trailing zeros
    for (digits = FRACDIGITS; digits > 0; digits--)
    {
        if ((fracpart % 10) != 0)
        {
            // last digit is not a zero
            break;
        }
        
        // Get rid of trailing zero
        fracpart /= 10;
    }

    // Print fractional part
    retval += print_int(printer, pstate, fracpart, false, digits, 10, "0123456789", true);

    if (exp > 0)
    {
        printer(pstate, 2, "e+");
        retval += 2;
        retval += print_int(printer, pstate, exp, false, 0, 10, "0123456789", false); 
    }

    return retval;
}
#endif /* HAVE_FLOAT */

static int32_t
lib_vprint(printfn printer, void *pstate, const char *pformat, va_list vaargs)
{
    int32_t  retval = 0;
    uint32_t val;
    float    fval;
    char    *sval;
    uint8_t  width = 0;
    bool     fmt, is_neg, zerofill;
    int      slen;

    while (*pformat)
    {
        if ((*pformat) == '%')
        {
            // Format command
            fmt = true;
            width = 0;
            zerofill = false;
            pformat++;

            while (fmt)
            {
                switch (*pformat)
                {
                case '0':
                    if (width == 0)
                    {
                        zerofill = true;
                        break;
                    }
                    // fall through
                case '1':
                case '2':
                case '3':
                case '4':
                case '5':
                case '6':
                case '7':
                case '8':
                case '9':
                    width *= 10;
                    width += *pformat - '0';
                    break;

                case 'c':
                    // Character

                    // Get character from vaargs
                    val = va_arg(vaargs, unsigned long);

                    // Print character
                    printer(pstate, 1, (char *)&val);
                    retval++;
                    
                    // Done with format command
                    fmt = false;
                    break;

                case 's':
                    // String

                    // Get string from vaargs
                    sval = va_arg(vaargs, char *);
                    slen = strlen(sval);

                    for (; width > slen; width--)
                    {
                        printer(pstate, 1, " ");
                        retval++;
                    }

                    printer(pstate, slen, sval);
                    retval += slen;

                    // Done with format command
                    fmt = false;
                    break;

                case 'd':
                case 'i':
                    // Integer

                    // Get number from vaargs
                    val = va_arg(vaargs, unsigned long);

                    is_neg = false;

                    // Check if it's negative
                    if (((long)val) < 0)
                    {
                        val = - ((long) val);
                        is_neg = true;
                    }

                    // Print number
                    retval += print_int(printer, pstate, val, is_neg, width, 10, "0123456789", zerofill);
                    
                    // Done with format command
                    fmt = false;
                    break;

                case 'u':
                    // Unsigned integer

                    // Get number from vaargs
                    val = va_arg(vaargs, unsigned long);

                    // Print number
                    retval += print_int(printer, pstate, val, false, width, 10, "0123456789", zerofill);

                    // Done with format command
                    fmt = false;
                    break;

                case 'p':
                    // Pointer

                    // Print "0x" first, incorrect with non-zero width
                    printer(pstate, 2, "0x");
                    retval += 2;
                    if (width > 2)
                    {
                        width -= 2;
                    }
                    else
                    {
                        width = 0;
                    }
                    // set zerofill to true due to incorrect width handling
                    zerofill = true;

                    // fall through
                case 'x':
                    // Hex integer

                    // Get number from vaargs
                    val = va_arg(vaargs, unsigned long);

                    // Print number
                    retval += print_int(printer, pstate, val, false, width, 16, "0123456789abcdef", zerofill);

                    // Done with format command
                    fmt = false;
                    break;

                case 'X':
                    // Hex integer

                    // Get number from vaargs
                    val = va_arg(vaargs, unsigned long);

                    // Print number
                    retval += print_int(printer, pstate, val, false, width, 16, "0123456789ABCDEF", zerofill);

                    // Done with format command
                    fmt = false;
                    break;
                    
#ifdef HAVE_FLOAT
                case 'f':
                    // Floating point

                    // Get number from vaargs
                    fval = (float) va_arg(vaargs, double);

                    // Print number
                    retval += print_flt(printer, pstate, fval);

                    // Done with format command
                    fmt = false;
                    break;
#endif /* HAVE_FLOAT */

                case '%':
                    // '%' character

                    printer(pstate, 1, "%");
                    retval++;

                    // Done with format command
                    fmt = false;
                    break;

                default:
                    // Error - can't handle other format commands/modifiers

                    return -1;
                }
                pformat++;
            }            
        }
        else
        {
            // Regular character
            printer(pstate, 1, pformat);
            retval++;
            pformat++;
        }
    }

    return retval;
}
