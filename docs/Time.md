# Time

The time module is designed to be loosely compatible with Python's, though it only supports two functions. Additionally, since the microcontroller doesn't have a real-time clock, it can only report relative time since startup.

sleep(n)
--------

Sleep for n seconds. n can be an integer or floating point number and is precise to approximately 10 milliseconds.

time()
------

Returns a floating point number representing the time since the microcontroller started in seconds.