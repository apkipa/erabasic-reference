**Summary**
- Despite the name, returns the first UTF-32 code value of the string as an integer.

**Tags**
- text

**Syntax**
- `UNICODEBYTE(str)`

**Signatures / argument rules**
- `UNICODEBYTE(str)` → `long`

**Arguments**
- `str` (string): source string.

**Semantics**
- Encodes `str` as UTF-32 and returns the first encoded code value.
- Only the first encoded code point matters; the remainder of the string is ignored.
- If the string begins with a supplementary character, the returned value can be greater than `0xFFFF`.
- This is a code-value query, not a raw-byte dump API.

**Errors & validation**
- Runtime error if `str == ""`.
- Any failure in the underlying UTF-32 conversion propagates as a runtime error.

**Examples**
- `UNICODEBYTE("A")` → `65`

**Progress state**
- complete
