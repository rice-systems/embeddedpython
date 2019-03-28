# Profiler

The profiler is not fully documented yet. Feel free to use it at your own risk.

callstats()
-----------

Returns information from the call statistics profiler. This is currently unfinished.

dict_profile()
---------------

Returns statistics from the dictionary profiler. This output does not need to be post-processed.

```
profile_function(f, frequency=100)
```

Sets up the profiler, starts it, runs function f, then stops it. The result should be passed through the profiler.py post-processor in the tools directory.

pystats()
---------

Dumps the results of the Python line number profiler. The results should be run through the pyprofiler.py post-processor.

reset()
-------

Resets all counters in the profiler. Run this before starting the profiler.

set_context()
--------------

Marks the current file as the one to profile for the line number profiler.

```
start(f=2001)
```

Starts the profiler with f ticks per second. This number should be relatively prime to the VM tick frequency. Picking a number that is itself prime is a good way to do this.

stop()
------

Stops the profiler.

vmstats()
---------

Dumps the results of the VM profiler. The results should be run through the profiler.py post-processor.