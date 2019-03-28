# Math

These math functions are direct maps to the C floating-point math library. They accept either floats or ints and return floats as the result.

acos(x)
-------

Returns the arc cosine of x, in radians.

asin(x)
-------

Returns the arc sine of x, in radians.

atan(x)
-------

Returns the arc tangent of x, in radians.

atan2(y, x)
-----------

Returns atan(y / x), in radians. The result is between -pi and pi. The vector in the plane from the origin to point (x, y) makes this angle with the positive X axis. The key feature of atan2() is that the signs of both inputs are known to it, so it can compute the correct quadrant for the angle. For example, atan(1) and atan2(1, 1) are both pi/4, but atan2(-1, -1) is -3\*pi/4.

cos(x)
------

Returns the cosine of x, in radians.

degrees(r)
----------

Converts the angle r from radians to degrees.

fabs(x)
-------

Returns the absolute value of x.

hypot(x, y)
-----------

Returns the Euclidean norm, sqrt(x\*x + y\*y). This is the length of the vector from the origin to point (x, y).

modf(x)
-------

Returns a tuple containing two elements: the fractional and integer parts of x, respectively. Both elements carry the sign of x and are floats.

pow(x, y)
---------

Returns x raised to the power y. Exceptional cases follow the schema of the C compiler used to build the VM. On the Cortex-M, pow(1.0, x) and pow(x, 0.0) always return 1.0, even when x is a zero or a NaN.

radians(d)
----------

Converts angle d from degrees to radians.

sin(x)
------

Returns the sine of x, in radians.

sqrt(x)
-------

Returns the square root of x. Returns floating-point infinity if x is negative.

tan(x)
------

Returns the tangent of x, in radians.