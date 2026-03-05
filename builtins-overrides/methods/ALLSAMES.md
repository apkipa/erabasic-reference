**Summary**
- Tests whether all arguments are equal to the first argument.

**Tags**
- math

**Syntax**
- `ALLSAMES(a, b [, c ...])`

**Signatures / argument rules**
- `ALLSAMES(a, b [, c ...])` → `long`
  - Requires at least 2 arguments.
  - All arguments must have the same type (int or string).

**Arguments**
- `a` (int|string)
- `b` (int|string)
- `c...` (optional, int|string)

**Semantics**
- Returns `1` if `a == b == c == ...`, otherwise returns `0`.

**Errors & validation**
- Parse-time error if the argument types do not match.

**Examples**
- `ALLSAMES(1, 1, 1)` returns `1`.
- `ALLSAMES(1, 1, 2)` returns `0`.

**Progress state**
- complete

