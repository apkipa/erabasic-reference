**Summary**
- Returns the base-10 logarithm of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `LOG10(x)`

**Signatures / argument rules**
- `LOG10(x)` → `long`

**Arguments**
- `x` (int): must be greater than `0`.

**Semantics**
- Computes `Math.Log10((double)x)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x <= 0`.
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `LOG10(1)` returns `0`.
- `LOG10(9)` returns `0`.
- `LOG10(10)` returns `1`.

**Progress state**
- complete

