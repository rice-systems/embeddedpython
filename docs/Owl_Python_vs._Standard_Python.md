# Owl Python vs. Standard Python

Owl is designed around Python 2.7 and uses the standard Python compiler. However, there are some features of Python that are not yet, and may never be, implemented in the Owl system. The following features are not available on Owl:

-   Exception handling
-   Generators or user-defined iterators
-   Operator overloading
-   Slice storing and deleting
-   Three element slicing
-   Keyword arguments
-   With statement
-   Exec statement

We have found that these features are not frequently used in the kinds of systems and applications developed for use on microcontrollers. For more details regarding the differences between Owl and standard Python, see below.

Exception handling
------------------

Owl has only a rudimentary exception system; while it offers complete error detection, the VM does not fully support error handling.

When an exception occurs at the interactive prompt, the error is reported back to the user, and the user can then type a new statement. If an exception occurs when the system is not connected to the desktop, the system will simply stop running. Any invalid code or runtime error *should* generate an exception. For example, the code “foo”\[5\] will generate an IndexError.

No code should be capable of *crashing* the virtual machine without an exception. Any code that does should be reported as a bug. The only exceptions to this are peripheral libraries. Invalid sequences of calls to these are capable of crashing the hardware itself.

Exceptions can be thrown by the VM itself; however, they cannot be thrown or caught by user code using the traditional syntax. Additional error handling functionality might be introduced sometime in the future.

Additionally, it is possible to generate an exception on demand using the [sys.raise_user_ex()](Sys "wikilink") function.

Generators, iterators and operator overloading
----------------------------------------------

There is rudimentary support for generators in the code, though they are unstable and are disabled by default. We do not currently have plans to fix them.

Iterator and operator overloading are also not supported. Currently, Owl only supports the special “__init__” object method. Others may be added if a real use for them presents itself.

Other features
--------------

Simple slicing, like a\[3:9\], a\[:3\] and a\[:\] are supported and work exactly like desktop Python. More complex slicing operations such as a\[3:6\] = \[1,2,3\], del a\[3:6\], a\[1:10:2\] are not currently and unlikely to ever be supported.

Since there aren't operating system resources such as sockets or files on the microcontroller, the “with” statement is also unlikely to be supported.

Finally, the “exec” statement and the compile function are not supported; they would require a compiler on the microcontroller, which is not currently planned.