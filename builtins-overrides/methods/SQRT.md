**Summary**
- Returns the square root of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `SQRT(x)`

**Signatures / argument rules**
- `SQRT(x)` → `long`

**Arguments**
- `x` (int): must be non-negative.

**Semantics**
- Computes `Math.Sqrt((double)x)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x < 0`.

**Examples**
- `SQRT(0)` returns `0`.
- `SQRT(2)` returns `1`.
- `SQRT(4)` returns `2`.

**Progress state**
- complete

