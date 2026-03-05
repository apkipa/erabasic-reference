**Summary**
- Returns a uniformly distributed random integer in a half-open range.

**Tags**
- math

**Syntax**
- `RAND(max)`
- `RAND(min, max)`

**Signatures / argument rules**
- `RAND(max)` → `long`
- `RAND(min, max)` → `long`

**Arguments**
- `min` (optional, int; default `0`): inclusive lower bound.
- `max` (int): exclusive upper bound.

**Semantics**
- Returns a random integer `r` such that `min <= r < max`.

**Errors & validation**
- Runtime error if `max <= min`.
  - In particular, `RAND(0)` and `RAND(<negative>)` are errors.

**Examples**
- `RAND(10)` returns a value in `0 <= r < 10`.
- `RAND(5, 8)` returns `5`, `6`, or `7`.

**Progress state**
- complete

