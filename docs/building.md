# Building Owl

This process describes how to build the Owl VM from scratch. If you're just '''using''' Owl and programming with the libraries that are already included, you don't need to do this. There's a much simpler process that allows you to documented on the [[The Owl Embedded Python System|main page]].

We've tested this process on 32-bit and 64-bit installs of Ubuntu 12.04 LTS.
The system can likely be built on any modern version of Linux that uses Python
2.7 as its default version.
 
* Ubuntu 12.04: http://www.ubuntu.com/
 
First, download the commercial packages that will be used to build Owl:

* CodeSourcery Lite: http://www.mentor.com/embedded-software/sourcery-tools/sourcery-codebench/editions/lite-edition/arm-eabi
* StellarisWare: http://www.ti.com/tool/sw-lm3s

Next, install the required Linux packages:
 
* $ sudo apt-get install ia32-libs libc6-dev-i386 libftdi-dev mercurial git python-yaml ccache
 
Install the compiler:
 
* $ sudo dpkg-reconfigure -plow dash
 
Select &lt;No&gt; for "Use dash as the default system shell"
 
* $ chmod a+x arm-2012.09-63-arm-none-eabi.bin
* $ ./arm-2012.09-63-arm-none-eabi.bin
* $ source ~/.profile
 
Perform a typical install.

You can now revert back to using DASH as your default sh shell:
 
* $ sudo dpkg-reconfigure -plow dash
 
Select &lt;Yes&gt; for "Use dash as the default system shell"

Now, we'll install StellarisWare. This can be done either through a Windows
computer, or we can use Wine. We'll do that here. Be sure to create a directory
for StellarisWare BEFORE starting the Windows-based installer, as wine's select
directory dialog box can't reliably create a directory.
 
* $ sudo apt-get install wine
* $ wine SW-LM3S-9453.exe
 
Now, we need to build it. Change directory into the StellarisWare directory you
created in the last step.
 
* $ cd usblib
* $ make
* $ cd ../driverlib
* $ make
 
We need to build the programmer:

* $ wget http://sourceforge.net/projects/openocd/files/openocd/0.6.0/openocd-0.6.0.tar.gz/download
* $ tar -zvxf download
* $ cd openocd
* $ ./configure --enable-ft2232_libftdi
* $ make
 
There's no need to actually ''install'' it. Our scripts refer to it in place.

Build libopencm3:
 
* $ git clone https://github.com/libopencm3/libopencm3.git
* $ cd libopencm3
* $ make
 
This will fail, but that's actually okay. It's compiled the parts we really care about.

The prerequisites are done. Let's actually get to building the virtual machine:

* $ hg clone https://bitbucket.org/ricearch/embeddedpython
* $ cd owl/src/platform/stellarisware
* $ cp Makefile.local.example Makefile.local
 
Edit this file to properly reflect the locations of StellarisWare and libopencm3.

* $ make
 
Finally, make a local copy of the programmer location definition:

* $ cd programmer
* $ cp programmer.local.example programmer.local
 
Edit this file to reflect your location of openocd. Finally, we're ready to
flash the controller:

* $ cd ..
* $ ./flash
 
Great! Now we're ready to [[Mcu|Connect to the Microcontroller]].
