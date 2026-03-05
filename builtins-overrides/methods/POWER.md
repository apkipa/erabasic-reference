**Summary**
- Returns `x^y` (x to the power y), truncated to an integer.

**Tags**
- math

**Syntax**
- `POWER(x, y)`

**Signatures / argument rules**
- `POWER(x, y)` → `long`

**Arguments**
- `x` (int)
- `y` (int)

**Semantics**
- Computes `Math.Pow((double)x, (double)y)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `POWER(2, 10)` returns `1024`.
- `POWER(2, -1)` returns `0`.

**Progress state**
- complete

