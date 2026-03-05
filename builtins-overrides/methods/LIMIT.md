**Summary**
- Clamps an integer value to a specified inclusive range.

**Tags**
- math

**Syntax**
- `LIMIT(value, min, max)`

**Signatures / argument rules**
- `LIMIT(value, min, max)` → `long`

**Arguments**
- `value` (int)
- `min` (int)
- `max` (int)

**Semantics**
- Returns:
  - `min` if `value < min`
  - `max` if `value > max`
  - otherwise `value`
- Note: `min` and `max` are used as written; they are not swapped if `min > max`.

**Errors & validation**
- (none)

**Examples**
- `LIMIT(5, 0, 10)` returns `5`.
- `LIMIT(-1, 0, 10)` returns `0`.
- `LIMIT(11, 0, 10)` returns `10`.

**Progress state**
- complete

