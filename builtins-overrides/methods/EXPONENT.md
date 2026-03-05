**Summary**
- Returns `e^x` (the exponential function), truncated to an integer.

**Tags**
- math

**Syntax**
- `EXPONENT(x)`

**Signatures / argument rules**
- `EXPONENT(x)` → `long`

**Arguments**
- `x` (int)

**Semantics**
- Computes `Math.Exp((double)x)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `EXPONENT(0)` returns `1`.
- `EXPONENT(1)` returns `2`.
- `EXPONENT(-1)` returns `0`.

**Progress state**
- complete

