**Summary**
- Counts how many of the trailing arguments are equal to the first argument.

**Tags**
- math

**Syntax**
- `GROUPMATCH(base, value1 [, value2 ...])`

**Signatures / argument rules**
- `GROUPMATCH(base, value1 [, value2 ...])` → `long`
  - Requires at least 2 arguments.
  - All arguments must have the same type (int or string).

**Arguments**
- `base` (int|string)
- `valueN` (int|string): values to compare against `base`.

**Semantics**
- Returns the number of `valueN` that compare equal to `base` using `==`.
- The first argument `base` is not counted as a match against itself.

**Errors & validation**
- Parse-time error if any `valueN` has a different type from `base`.

**Examples**
- `GROUPMATCH(1, 1, 2, 1)` returns `2`.
- `GROUPMATCH("a", "a", "b")` returns `1`.

**Progress state**
- complete

