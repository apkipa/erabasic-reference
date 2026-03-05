**Summary**
- Returns the natural logarithm of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `LOG(x)`

**Signatures / argument rules**
- `LOG(x)` → `long`

**Arguments**
- `x` (int): must be greater than `0`.

**Semantics**
- Computes `Math.Log((double)x)` (base *e*) and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x <= 0`.
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `LOG(1)` returns `0`.
- `LOG(2)` returns `0` (since `ln(2)` is between `0` and `1`).

**Progress state**
- complete

