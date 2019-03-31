# Built-in Library

The built-in library defines the built-in default namespace. This default namespace contains those functions which can always be accessed anywhere.

```
HEXDIGITS = '0123456789abcdef'
```

A string consisting of all hex digits, used internally to check if something is a valid hex digit. Slicing it will allow you to test any base: ```HEXDIGITS[:base]```.

abs(n)
------

Return the absolute value of a number. The argument may be either an integer or a floating point number.

address(o)
----------

Returns the memory address of object o.

all(iterable)
-------------

Returns True if all objects in iterable evaluate to True (see [bool()](#boolo)).

any(iterable)
-------------

Returns True if at least one of the objects in iterable evaluates to True (see [bool()](#boolo)).

bool(o)
-------

Converts a value to a Boolean, using the [standard truth testing procedure](http://docs.python.org/2.7/library/stdtypes.html#truth).

chr(n)
------

Returns a string of one character whose ASCII code is the integer n. For example, chr(97) returns the string 'a'. The argument must be in the range \[0..255\], inclusive; a ValueError will be raised if n is outside that range. This is the inverse of [ord()](#ords).

cmp(obj1, obj2)
---------------

Compares the two objects obj1 and obj2 and returns an integer corresponding to the outcome. The return value is negative if obj1 &lt; obj2, zero if obj1 == obj2 and strictly positive if obj1 &gt; obj2.

copy(o)
-------

Performs a shallow copy of the object o, returning the new copy.

dir(space=None)
---------------

Without arguments, returns the list of names in the current local scope. With an argument, attempts to return a list of valid attributes for that object.

enumerate(l)
------------

Returns a list of tuples where each tuple contains one element from l and its index. For example:

```
>>> enumerate(['a', 'b', 'c'])

[(0, 'a'), (1, 'b'), (2, 'c')]
```

eval(co, g, l)
--------------

Evaluates a code object co, optionally accepting a globals dict g and a locals dict l.

filter(f, s)
------------

Constructs a list containing those elements from s for which f returns True.

float(s)
--------

Converts a string or a number to floating point. If the argument is a string, it must contain a (possibly signed) decimal or floating point number, possibly embedded in whitespace. Otherwise, the argument may be a plain or long integer or a floating point number, in which case a floating point number with the same value (within Python's floating point precision) is returned. If no argument is given, returns 0.0.

globals()
---------

Returns a dictionary representing the current global symbol table. This is always the symbol table of the current module. Inside a function or method, the “current” module is the module where that function is defined, *not* the module from which it is called.

hex(i)
------

Converts an integer number (of any size) to a hexadecimal string. The result is a valid Python expression.

int(x, base)
------------

Converts the number or string x to an integer, or returns 0 if no arguments are given. If x is a number, it can be a plain integer, a long integer, or a floating point number. For floating points, the conversion truncates towards zero.

If x is not a number, then x must be a string representing an integer literal in radix base. Optionally, this string can be preceded by + or - (with no space in between) and surrounded by whitespace.

The default base is 10; allowed values are 0 and 2-36. Note that if the optional base argument is provided, x must be a string, not a number. A base-n literal consists of the digits 0 to n-1, with a to z (or A to Z) having values 10 to 35. Base-2, -8, and -16 literals can be optionally prefixed with 0b/0B, 0o/0O/0, or 0x/0X, respectively, as with integer literals in code. Base 0 means to interpret the string exactly as an integer literal, so that the actual base is 2, 8, 10, or 16.

ismain()
--------

Returns True if the current module is the top-level module loaded by the device. This can be useful to test whether a program is being loaded from the interactive prompt, or directly at microcontroller start.

len(s)
------

Returns the length (number of items) in the object s. The argument may be a sequence (string, tuple or list) or a mapping (dictionary).

locals()
--------

Returns the dictionary representing the local symbol table of the running module.

map(function, iterable)
-----------------------

Applies function to every element of iterable and returns a list of the element-wise results.

max(iterable)
-------------

Returns the largest item in iterable.

min(iterable)
-------------

Returns the smallest item in iterable.

ord(s)
------

Given a string of length one, returns an integer representing the value of the byte when the argument is represented as an 8-bit string. For example, ord('a') returns the integer 97. This is the inverse of [chr()](#chrn).

pow(x, y)
---------

Returns x raised to the power y.

raise_user_ex(n)
------------------

Throws the object n as the information for a UserException exception. For example, this could be a constant string: raise_user_ex(“robot on fire!”), or a variable: n=4000; raise_user_ex(“robot internal temperature is %d degrees” % n).

str(n)
------

Returns a string representation of the object n.

```
range(a, b=None, c=None)
```

This is an alias to [xrange()](#xrange).

sum(s)
------

Returns the sum of all elements of s.

type(o)
-------

Returns an integer representing the [internal type code](Types "wikilink") of o.

```
xrange(start=None, stop, step=None)
```

This is a versatile function used to create xrange containing arithmetic progressions. It is most often used in for loops. The arguments must be plain integers. If the step argument is omitted, it defaults to 1. If the start argument is omitted, it defaults to 0.

The full form returns a generator of plain integers \[start, start + step, start + 2 \* step, ...\]. If step is positive, the last element is the largest start + i \* step less than stop; if step is negative, the last element is the smallest start + i \* step greater than stop. step must not be zero (or else ValueError is raised).