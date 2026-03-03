**Summary**
- Converts a string to uppercase.

**Documentation depth**
- High: direct mapping to engine implementation (including null/empty handling and casing rules).

**Syntax**
- `TOUPPER(str)`

**Signatures / argument rules**
- `TOUPPER(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: returns `str.ToUpper()` using the process `CurrentCulture`.
  - In this engine, `CurrentCulture` is set to `InvariantCulture` at startup, so behavior is invariant-culture uppercasing.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOUPPER("Abc")` → `"ABC"`

**Progress state**
- complete
