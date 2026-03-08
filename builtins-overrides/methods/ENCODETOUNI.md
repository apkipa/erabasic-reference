**Summary**
- Returns the Unicode scalar value at a UTF-16 position in a string.

**Tags**
- text

**Syntax**
- `ENCODETOUNI(str [, position])`

**Signatures / argument rules**
- `ENCODETOUNI(str)` → `long`
- `ENCODETOUNI(str, position)` → `long`

**Arguments**
- `str` (string): source string.
- `position` (optional, int; default `0`): UTF-16 code-unit index.

**Semantics**
- If `str == ""`, returns `-1` immediately, even if `position` is supplied.
- Otherwise returns `.NET` `char.ConvertToUtf32(str, position)`.
- `position` counts UTF-16 code units, not Unicode scalar values.
- If a supplementary character begins at `position`, the returned value can be greater than `0xFFFF`.
- If `position` points at the second half of a surrogate pair, or at another invalid UTF-16 sequence, conversion fails with a runtime error.

**Errors & validation**
- Runtime error if `str != ""` and `position < 0`.
- Runtime error if `str != ""` and `position >= str.Length`.
- Runtime error if UTF-16 to scalar conversion fails at the requested position.

**Examples**
- `ENCODETOUNI("A")` → `65`

**Progress state**
- complete
