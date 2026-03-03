**Summary**
- Converts a string to lowercase.

**Documentation depth**
- High: direct mapping to engine implementation (including null/empty handling and casing rules).

**Syntax**
- `TOLOWER(str)`

**Signatures / argument rules**
- `TOLOWER(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: returns `str.ToLower()` using the process `CurrentCulture`.
  - In this engine, `CurrentCulture` is set to `InvariantCulture` at startup, so behavior is invariant-culture lowercasing.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOLOWER("Abc")` → `"abc"`

**Progress state**
- complete
