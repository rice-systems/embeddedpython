mcu is the command line utility that is used to interact with the microcontroller running the virtual machine. It is used to enter [interactive mode](IPM "wikilink") and to flash modules onto the system. It is also used to run the desktop version of the virtual machine for testing without a microcontroller.

The first thing you will likely want to do is connect to the microcontroller with an interactive prompt. This page explains how to do that.

Invoking mcu
------------

The invocation of mcu is:

       mcu -[s /dev/tty] --[serial=/dev/tty [baud=19200]
                [ image.bin | foo.py, bar.py, ... | [ ipm | desktop ] ]

The first two arguments (--serial and baud) are optional. mcu will attempt to autodetect a connected microcontroller on both Linux and OS X. If it cannot, the --serial argument should be set to the virtual serial port that the microcontroller is connected to. To identify the correct device, look for a device in dev starting with “tty” that disappears and reappears when you plug and unplug the microcontroller. Run the following command with and without the microcontroller connected:

-   $ ls /dev/tty\*

Starting IPM
------------

To start [IPM](IPM "wikilink"), connect the controller, reset it and run mcu with the “ipm” command:

-   $ mcu ipm

This will bring you to the interactive prompt. Here, you can type individual statements, define and execute functions and run single files. See the [IPM](IPM "wikilink") page for more detail.

Starting the desktop interpreter
--------------------------------

The mcu command can also start the desktop version of Owl. This runs the exact same virtual machine as the microcontroller does, so that you can experiment with the differences between [Owl Python and standard Python](Owl_Python_vs._Standard_Python "wikilink") without having a microcontroller. Note that the desktop VM does not have the peripheral libraries that the controller version does. To start the desktop VM and connect to it, type:

-   $ mcu desktop

Flashing programs
-----------------

Finally, mcu is used to program modules to the microcontroller. These modules can be imported by name, either from the [interactive prompt](IPM "wikilink") or from another module. Flashing modules is simple:

-   $ mcu main.py second.py third.py

This process overwrites any user-flashed modules that have previously been written to the microcontroller. In other words, each time you flash the controller, you should include *all* modules used by your program. Note that built-in modules are part of the virtual machine, and should not be listed when flashing a program.

In the above example, three modules were flashed. The module named “main” can import the other two with the statements:

-   import second
-   import third

Finally, since “main” was the first module listed when the microcontroller was flashed, it becomes the main module on the microcontroller. This is the module that is run first when the microcontroller is powered up and the system button is pressed. This should be the top level of your program itself.