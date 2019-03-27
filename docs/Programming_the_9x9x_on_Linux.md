The following process has been tested on both 32- and 64-bit installs of Ubuntu 12.04 LTS. The system can likely be built on any modern version of Linux that uses Python 2.7 as its default version.

First, you should have installed the [User tools on Linux](User_tools_on_Linux "wikilink").

Next, you should install OpenOCD, which is used to program the target. This has been well tested with both versions 0.6.0 and 0.6.1. To install OpenOCD:

-   $ wget [1](http://sourceforge.net/projects/openocd/files/openocd/0.6.0/openocd-0.6.0.tar.gz/download)
-   $ tar -zvxf download
-   $ cd openocd
-   $ ./configure --enable-ft2232_libftdi
-   $ make
-   $ sudo make install

Now, download the appropriate [VM binary for your microcontroller](Downloads "wikilink") as well as the flash-vm script. Reset the chip and program it:

-   $ cd flash-vm
-   $ ./flash-vm path/to/the/vm/binary

If the ./flash-vm command doesn't finish within thirty seconds or so, cancel it (Ctrl-C) and try it again *without* resetting the chip. You should now be able to [connect to the microcontroller](mcu "wikilink")!