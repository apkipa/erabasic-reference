**Summary**
- Tests whether a value is within an inclusive numeric range.

**Tags**
- math

**Syntax**
- `INRANGE(value, min, max)`

**Signatures / argument rules**
- `INRANGE(value, min, max)` → `long`

**Arguments**
- `value` (int)
- `min` (int)
- `max` (int)

**Semantics**
- Returns `1` if `min <= value <= max`, otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `INRANGE(5, 0, 10)` returns `1`.
- `INRANGE(10, 0, 10)` returns `1`.
- `INRANGE(11, 0, 10)` returns `0`.

**Progress state**
- complete

