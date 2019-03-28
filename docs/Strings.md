# Strings

Strings in Owl work exactly as they do in Python 2.7: they are ordered collections of bytes that may include NULL characters. However, they do not support Unicode. Since Owl uses the Python compiler, any of the many forms of string literals are understood by Owl. See [the Python string documentation](http://docs.python.org/2/tutorial/introduction.html#strings) for more details.

Finally, zero, one and two element slicing is supported. Three element slicing is not and is unlikely to ever be supported. Again, see [the Python string documentation](http://docs.python.org/2/tutorial/introduction.html#strings) for more details.

String methods
--------------

The _str module defines the object methods for all strings. All methods defined within it should be called directly on a string object:

```
>>> a = "foo"
>>> print a.count('o')
3
```

### s.count(s1, start=0, end=len(s))

Returns the number of non-overlapping occurrences of substring s1 in the slice s\[start:end\]. Optional arguments start and end are interpreted as in slice notation, with start being inclusive and end being exclusive. Thus, these default to 0 and len(s), respectively.

### s.find(s1, start=0, end=len(s))

Returns the lowest index in the string where substring s1 is found, such that s1 is contained in the slice s\[start:end\]. Optional arguments start and end are interpreted as in slice notation, with start being inclusive and end being exclusive. Thus, these default to 0 and len(s), respectively. Returns -1 if s1 is not found.

### s.join(l)

Returns a string which is the concatenation of the strings in the iterable l. The separator between elements in l is the string s providing this method.

### s.split(s1=None)

Returns a list of the words in the string s, using s1 as the delimiter string between words.

If s1 is given, consecutive delimiters are not grouped together and are deemed to delimit empty strings (for example, '1,,2'.split(',') returns \['1', *, '2'\]). Note that the sep argument may consist of multiple characters; for example, '1&lt;&gt;2&lt;&gt;3'.split('&lt;&gt;') returns \['1', '2', '3'\]. Splitting an empty string with a specified separator returns \[*\].

If s1 is not specified or is None, a different splitting algorithm is applied: runs of consecutive whitespace are regarded as a single separator, and the result will contain no empty strings at the start or end if the string has leading or trailing whitespace. Consequently, splitting an empty string or a string consisting of just whitespace with a None separator returns \[\].

### s.strip()

Returns a copy of the string with the leading and trailing whitespace removed.