# SimpleGPIO

SimpleGPIO provides a cross-platform, easy to use GPIO library. It does not provide all the low-level features of the [low level GPIO interface](List_of_Stellaris_driver_libraries "wikilink"), but it is sufficient for interfacing with the vast majority of simple devices.

Example
-------

```
>>> import simplegpio
>>> button = simplegpio.Input('a1', simplegpio.PULLUP)
>>> button.read()
True
>>> led = simplegpio.Output('a2')
>>> led.on()
```

Initializers
------------

To initialize a pin, you must call the constructor for an input or output:

```
o = simplegpio.Output(portpin)
i = simplegpio.Input(portpin, type)
```

This routine will set up the selected GPIO subsystem, set the correct pin type and return a SimpleGPIO object. 'portpin' is a two-character string naming the desired device, such as 'a1' or 'd6'. (Lower-case letters should be used.)

When defining an input, 'type' must be simplegpio.INPUT for a floating input, simplegpio.PULLUP for a weak pull-up and simplegpio.PULLDOWN for a weak pull-down. These pull-up/pull-down modes are appropriate for mechanical switches.

GPIO class Methods
------------------

Input SimpleGPIO objects have one method:

```
i.read()
```

This method returns True if the pin is at a logical 1 and False if the pin is at a logical 0.

Output SimpleGPIO objects have three methods:

```
o.on()
o.off()
o.write(value)
```

Here, value can be any type. If value evaluates to True (typically the integer 1 or the boolean True), the pin will be driven high. If value is False, it will be driven low.