**Summary**
- Tests whether all arguments are pairwise distinct.

**Tags**
- math

**Syntax**
- `NOSAMES(a, b [, c ...])`

**Signatures / argument rules**
- `NOSAMES(a, b [, c ...])` → `long`
  - Requires at least 2 arguments.
  - All arguments must have the same type (int or string).

**Arguments**
- `a` (int|string)
- `b` (int|string)
- `c...` (optional, int|string)

**Semantics**
- Returns `1` if no two arguments are equal (using `==`), otherwise returns `0`.

**Errors & validation**
- Parse-time error if the argument types do not match.

**Examples**
- `NOSAMES(1, 2, 3)` returns `1`.
- `NOSAMES(1, 2, 1)` returns `0`.

**Progress state**
- complete

