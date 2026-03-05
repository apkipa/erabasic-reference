**Summary**
- Returns the sign of an integer.

**Tags**
- math

**Syntax**
- `SIGN(x)`

**Signatures / argument rules**
- `SIGN(x)` → `long`

**Arguments**
- `x` (int)

**Semantics**
- Returns:
  - `-1` if `x < 0`
  - `0` if `x == 0`
  - `1` if `x > 0`

**Errors & validation**
- (none)

**Examples**
- `SIGN(-10)` returns `-1`.
- `SIGN(0)` returns `0`.
- `SIGN(10)` returns `1`.

**Progress state**
- complete

