# The Owl Embedded Python System

The Owl Embedded Python System is a free and open-source system for programming small 32-bit microcontrollers in Python. It is dramatically easier to use than other programming environments for microcontrollers, while still powerful enough to build just about anything. Try it out today!

Owl is currently in a limited release. Right now, we have released VM binaries for TI Stellaris microcontrollers and the user toolchain as well as the complete source code. This is enough to get started programming microcontrollers, though there are more pieces yet to be released:

If you have any questions about Owl, contact us at [mailto:twb@embeddedpython.org twb@embeddedpython.org]

## Manifesto
 
Modern microcontrollers are almost always programmed in C. Applications run at a very low level without a real operating system. They are painfully difficult to debug, analyze, and maintain. At best, a simple real-time operating system (RTOS) is used for thread scheduling, synchronization, and communication. These systems provide primitive, low-level mechanisms that require expert knowledge to use and do very little to simplify programming. At worst, they are programmed on the bare metal, perhaps even without a C standard library. As the the electronic devices of the world become more and more complex, we absolutely have to do something to make embedded development easier.

We believe that the best way to do this is to run embedded software on top of a managed run-time system. We have developed and released as open-source an efficient embedded Python programming environment named Owl. Owl is a complete Python development toolchain and run-time system targeting systems that lack the resources to run a traditional operating system, but are still capable of running sophisticated software systems.
Owl is a complete system, including an interactive development environment, a set of profilers, and an interpreter. It is derived from portions of several open-source projects, including CPython and Baobab. Most notably, the core run-time system for Owl is a modified version of Dean Hall's Python-on-a-Chip.

Overall, we believe that Owl is the most productive, easy-to-use system in the world for programming small computers.

## Installing Owl
 
The easiest way to learn about Owl is to dive in and get started. It's easy and fun! First, install the command-line user utilities from the Python Package Index (PyPI) and easy_install. This should work out of the box on any system already running Python 2.7, including any recent version of Linux or OS X.

* sudo easy_install owl-tools
 
Next, make sure that you are using a microcontroller that is supported by Owl. Currently, the only chips supported are the TI Stellaris LM3S9x9x series. We've tested the platform on other chips and they will be supported soon. If you can't wait that long, help us out by porting it!
 
* [[Programming the 9x9x on Linux]]
* [[Programming the 9x9x on Mac OS X]]
 
Finally, you're ready to [[mcu|connect to the microcontroller]]!

## Using Owl
 
Once you have Owl installed, you'll want to get started. Owl is very similar to normal Python. If you know Python already, you should be just about ready to get started. If you don't, it's an easy language to pick up. The official [http://docs.python.org/2/tutorial/ Python tutorial] is a great introduction, and most of what you read there should be applicable to Owl. Hordes of first-semester freshmen have learned their first Python (and generally their first programming) on Owl over the past few years, so you can too.

To connect to the microcontroller, you will use the [[mcu]] utility to start the [[IPM|interactive prompt]].

Of course, just using a microcontroller as a computer isn't much fun. We want to interact with the world. Owl comes with driver libraries to do exactly that. Take a look at the pages linked below to see what you can do.
 
* [[Owl Python vs. Standard Python]]
* [[List of Owl system libraries and object methods]]
* [[List of High-level driver libraries]]
* [[List of Stellaris driver libraries]]

## Hacking with Owl

Owl is open-source, published on [https://bitbucket.org/ricearch/embeddedpython BitBucket]. It can be freely copied, modified and distributed. Let us know what you're doing with it!

* [Building Owl](building.md)
