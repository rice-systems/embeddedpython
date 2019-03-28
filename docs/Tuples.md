# Tuples

Tuple methods
-------------

The _tuple modules defines the object methods for all tuples. It shouldn't be used directly. Instead, these methods should be called directly on a tuple object:

```
>>> a = (1, 2)
>>> print a.index(2)
1
```

### index(t, o)

Finds the first element of l equal to o. If no elements are equal to o, return -1.