Owl supports a version of Python's set type. A set is an unordered collection with no duplicate elements. Basic uses include membership testing and eliminating duplicate entries. Set objects also support mathematical operations like union and intersection.

Curly braces or the set() function can be used to create sets. Note that to create an empty set you have to use set(), not {}; the latter creates an empty [dictionary](Dictionaries "wikilink").

`>>> a = set([1, 2, 3])`
`>>> a = {1, 2, 3}`
`>>> print a`
`set([1, 2, 3])`

Set methods
-----------

The _set modules defines the object methods for all sets. All methods defined within it should be called directly on a set object:

`>>> a = set([1, 2, 3])`
`>>> a.add(4)`
`>>> print a`
`set([1, 2, 3, 4])`

### s.add(o)

Adds element s to set o.

### s.difference(s1)

Finds and returns a set containing the elements that appear in either s or s1, but not both.

### s.discard(o)

Removes element o from the set s if it is present.

### s.intersection(s1)

Finds and returns a set containing the elements that appear in both s or s1.

### s.remove(o)

Removes element o from the set s. Raises a KeyError if o is not contained in the set.

### s.union(s1)

Returns a new set containing all elements that appear in either s or s1.