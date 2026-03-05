**Summary**
- Returns the cube root of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `CBRT(x)`

**Signatures / argument rules**
- `CBRT(x)` → `long`

**Arguments**
- `x` (int): must be non-negative.

**Semantics**
- Computes `Math.Pow((double)x, 1.0 / 3.0)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x < 0`.

**Examples**
- `CBRT(0)` returns `0`.
- `CBRT(7)` returns `1`.
- `CBRT(8)` returns `2`.

**Progress state**
- complete

