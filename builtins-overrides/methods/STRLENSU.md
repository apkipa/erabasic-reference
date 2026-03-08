**Summary**
- Returns the length of a string in UTF-16 code units.

**Tags**
- text

**Syntax**
- `STRLENSU(str)`

**Signatures / argument rules**
- `STRLENSU(str)` → `long`

**Arguments**
- `str` (string): input string.

**Semantics**
- Returns the same count that command-form `STRLENU` would write to `RESULT`.
- Equivalent to `.NET` `string.Length`.
- BMP characters count as `1`.
- Supplementary characters count as `2` because they occupy a UTF-16 surrogate pair.

**Errors & validation**
- None.

**Examples**
- `STRLENSU("ABC")` → `3`

**Progress state**
- complete
