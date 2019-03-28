# Sys

These functions are found in the system module, and should be used with caution.

_modules()
-----------

Returns the module cache.

_sleep_until(n)
-----------------

Sleeps until the system time equals n. Avoid calling this function, [sys.sleep()](#sleepn), or [sys.time()](#time) directly; rather, use the functions in [time](Time "wikilink"), which are consistent with the versions used in traditional Python.

exit(val)
---------

Exits the interpreter. This is only really on platforms that can exit, such as the desktop VM.

gcRun()
-------

Immediately forces a garbage collector run.

getb()
------

Gets a byte from the host. Both getb() and [sys.putb()](#putbb) work as direct interfaces to the USB connection, and therefore are primarily used by IPM. However, they are also usable if you're running a program that does not work through IPM: without IPM, the connection to Owl should appear as the device /dev/mcu. You can manually open this file and write bytes to it, which will then be retrieved from /dev/mcu by a call to getb().

heap()
------

Returns a tuple containing the number of bytes used in the heap and the total number of bytes the heap can hold.

printFreeList()
---------------

Prints the garbage collector's free list. Note that the garbage collector may run before this functions gets called.

putb(b)
-------

Puts a byte to the host. Like [sys.getb()](#getb), putb() is generally used with IPM. However, it can be used without IPM to put bytes to /dev/mcu.

sleep(n)
--------

Sleeps for n milliseconds. Avoid calling this function, [sys._sleep_until()](#_sleep_until), or [sys.time()](#time) directly; rather, use the functions in [time](Time "wikilink"), which are consistent with the versions used in traditional Python.

time()
------

Returns the time, in milliseconds, since the microcontroller was powered on. Note that this includes time spent in the bootloader. Avoid calling this function, [sys._sleep_until()](#_sleep_until), or [sys.sleep()](#sleepn) directly; rather, use the functions in [time](Time "wikilink"), which are consistent with the versions used in traditional Python.