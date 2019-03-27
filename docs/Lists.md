List methods
------------

The _list module defines the object methods for all lists. All methods defined within it should be called directly on a list object:

`>> a = [1, 2, 3]`
`>>> a.append(4)`
`>>> print a`
`[1, 2, 3, 4]`

### l.append(o)

Appends object o to the list l.

### l.clear()

Empties all elements from list l.

### l.count(v)

Returns the number of occurrences of v in l.

### l.extend(s)

Appends all elements from s onto l, preserving the order of the elements in s.

### l.index(o)

Finds the first element of l that is equal to o. If no elements are equal to o, returns -1.

### l.insert(i, o)

Inserts element i after the o-th element of l.

=== l.pop(i=-1) ===

Removes and returns the i-th element from the list l, where i defaults to the last element in the list.

### l.remove(v)

Removes the first occurrence of v from list l.