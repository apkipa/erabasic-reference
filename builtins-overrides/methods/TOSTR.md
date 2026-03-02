**Summary**
- Converts an integer to a string, optionally using a .NET numeric format string.

**Signatures / argument rules**
- `TOSTR(i)` → `string`
- `TOSTR(i, format)` → `string`

**Arguments**
- `i`: int expression.
- `format` (optional): string expression passed to `Int64.ToString(format)`.

**Semantics**
- If `format` is omitted or null: returns `i.ToString()`.
- Otherwise: returns `i.ToString(format)`.

**Errors & validation**
- Errors if `format` is not a valid numeric format string.

**Examples**
- `TOSTR(42)` → `"42"`
- `TOSTR(42, "D5")` → `"00042"`
