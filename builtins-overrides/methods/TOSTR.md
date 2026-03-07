**Summary**
- Converts an integer to a string, optionally using a .NET numeric format string.

**Tags**
- text

**Syntax**
- `TOSTR(i [, format])`

**Signatures / argument rules**
- `TOSTR(i)` → `string`
- `TOSTR(i, format)` → `string`

**Arguments**
- `i` (int): value to format.
- `format` (optional, string; default `""`): numeric format string passed to `Int64.ToString(format)`.

**Semantics**
- Empty `format` uses default formatting.
- Otherwise returns `i.ToString(format)`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- If `format` is present but not a valid `.NET` numeric format string, raises a runtime error for invalid format (engine reports the error at argument position 2).

**Examples**
- `TOSTR(42)` → `"42"`
- `TOSTR(42, "D5")` → `"00042"`

**Progress state**
- complete
