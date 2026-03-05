**Summary**
- Returns the absolute value of an integer.

**Tags**
- math

**Syntax**
- `ABS(x)`

**Signatures / argument rules**
- `ABS(x)` → `long`

**Arguments**
- `x` (int)

**Semantics**
- Returns `Math.Abs(x)`.

**Errors & validation**
- Runtime error if `x == -9223372036854775808` (the minimum `Int64`), because `ABS(x)` would overflow.

**Examples**
- `ABS(-3)` returns `3`.
- `ABS(3)` returns `3`.

**Progress state**
- complete

