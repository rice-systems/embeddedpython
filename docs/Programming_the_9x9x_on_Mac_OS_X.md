To program the virtual machine to the microcontroller on UNIX-like systems (including OS X), we use OpenOCD. It is easy to install through MacPorts. It is possible to install OpenOCD without MacPorts, though it is *very* tricky and that process is not described here.

Start by downloading Xcode throught the Mac App Store. It's quite large, though free. Once you've installed that, start Xcode and install the command line tools. See [this article](http://developer.apple.com/library/ios/#documentation/DeveloperTools/Conceptual/WhatsNewXcode/Articles/xcode_4_3.html) for more details. Next [download and install MacPorts](http://www.macports.org/install.php).

Next, we need to actually install OpenOCD. From a terminal window, type:

-   $ sudo port install openocd

Now, download the appropriate [VM binary for your microcontroller](Downloads "wikilink") as well as the flash-vm script. Reset the chip and program it:

-   $ cd flash-vm
-   $ ./flash-vm path/to/the/vm/binary

We've found this to be reliable. If it doesn't finish within thirty seconds or so, cancel it (Ctrl-C) and try it again **without** resetting the chip. You should now be able to [connect to the Microcontroller](mcu "wikilink")!