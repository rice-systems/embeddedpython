# IPM

The heart of the Owl system is the interactive prompt, IPM. IPM originally comes from Dean Hall's [p14p project](https://code.google.com/p/python-on-a-chip/) where it stood for "Interactive PyMite".

In essence, it acts exactly like the standard Python prompt. You can use it to test out code at run-time and explore how your programs will work. You can type a statement (or a group of statements), and see the results. Go ahead and try it out! You can define functions, import modules, call driver libraries, anything you can do with standard Python prompt.

Users should beware of some specific differences, however, between the IPM facility and the desktop Python interpreter.
 
## Running programs are uninterruptable
 
On standard Python, pressing Ctrl-C will interrupt a running program. This is not the case in Owl. If the system becomes unresponsive, you should reset the controller by pressing the attached reset button. This should cause IPM to exit immediately. If it does not, press Ctrl-C to return to the prompt, then Ctrl-D to disconnect.
 
## Exceptions are abbreviated by default
 
When an exception occurs, the system only shows the information about the user program where the exception occurred. To get more detail about the exception, the user can type "verbose" at the prompt to get more info:

<code>python&gt; "abc"[5] <br>
Index error <br>
File &lt;interactive&gt;, line 1 <br>
Thread ID: 3 <br>
python&gt; verbose <br>
Error &#160;: Index error <br>
File &#160;: seq.c <br>
Line &#160;: 232 <br>
Python File&#160;: &lt;interactive&gt; <br>
Python Line&#160;: 1 <br>
Info &#160;: <br>
Thread ID &#160;: 3 <br>
Traceback (top first)&#160;: <br>
-&lt;interactive&gt;() <br>
-ipm() <br>
-main() <br>
-&lt;module&gt;. <br> </code>
 
## Run command
 
To make developing modules easier, IPM includes a ''run'' command. This command takes a file and executes the entire file in the local scope. It is as if each line from the file was typed, one at a time at the prompt. You should remember that when you run a file, it cannot be interrupted without resetting the microcontroller. It should run once, then exit on its own.

Using this facility, you can run a file, edit it, then run it again without resetting the core.

<code>python&gt; run test.py <br>
hello world <br>
python&gt; <br> </code>
