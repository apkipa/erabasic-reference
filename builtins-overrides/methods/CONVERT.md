**Summary**
- Converts an integer to its string form in base `2`, `8`, `10`, or `16`.

**Tags**
- text

**Syntax**
- `CONVERT(value, toBase)`

**Signatures / argument rules**
- `CONVERT(value, toBase)` → `string`

**Arguments**
- `value` (int): value to format.
- `toBase` (int): output base.

**Semantics**
- Accepts only `2`, `8`, `10`, or `16` for `toBase`.
- Equivalent to `.NET` `Convert.ToString(value, toBase)`.
- For hexadecimal output, alphabetic digits follow the external `.NET` behavior (`a`-`f`).

**Errors & validation**
- Runtime error if `toBase` is any value other than `2`, `8`, `10`, or `16`.

**Examples**
- `CONVERT(255, 16)` → `"ff"`

**Progress state**
- complete
