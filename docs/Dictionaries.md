# Dictionaries

Owl includes a minimal version of the Python dictionary type. For more information on standard Python dictionaries, see the [Python documentation](http://docs.python.org/2/tutorial/datastructures.html#dictionaries).

Dictionaries are sometimes found in other languages as associative memories or associative arrays. Unlike sequences, which are indexed by a range of numbers, dictionaries are indexed by keys, which can be any immutable type. For instance, strings and numbers can always be keys. Tuples can be used as keys if they contain only strings, numbers, or tuples; however, if a tuple contains any mutable object either directly or indirectly, it cannot be used as a key. Lists can't be keys, since they can be modified in place using index assignments, slice assignments, or methods like append() and extend().

It is best to think of a dictionary as an unordered set of key:value pairs, with the requirement that the keys within a single dictionary are unique. A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output. Currently, dictionaries in Owl do have an order, though this may not always be true.

The main operations on a dictionary are storing a value associated with some key and extracting the value given the key. It is also possible to delete a key:value pair with del. If you store using a key that is already in use, the old value associated with that key is forgotten. It is an error to extract a value using a non-existent key.

It should be noted that unlike traditional Python implementations, dictionaries in Owl do not use hash tables. This means that they take up less memory, but are significantly slower. Accessing and updating dictionaries all take O(n) time where n is the size of the dictionary.

Creating dictionaries
---------------------

The typical way to create a dictionary is to use the dictionary literal:

```
>>> a = {'a':1, 'b':2}
>>> print a
{'a':1, 'b':2}
```

Dictionary methods
------------------

The _dict module defines the object methods for all dictionaries. All methods defined within it should be called directly on a dictionary object:

```
>>> a = {'a':1, 'b':2}
>>> a.keys()
['a', 'b']
```

### d.clear()

Empties the dictionary of all mappings.

### d.has_key(k)

Returns True if the dictionary has key k, false otherwise.

### d.keys()

Returns a list of all keys in the dictionary.

### d.pop(k)

Removes the k-th element of the dictionary and returns it. Unlike traditional Python, dictionaries in Owl are ordered, so this yields predictable results.

### d.values()

Returns a list of all values in the dictionary.