**Summary**
- Escapes a string so it can be used as literal text inside regex-based built-ins.

**Tags**
- text

**Syntax**
- `ESCAPE(str)`

**Signatures / argument rules**
- `ESCAPE(str)` → `string`

**Arguments**
- `str` (string): input text.

**Semantics**
- Equivalent to `.NET` `Regex.Escape(str)`.
- Escapes regex metacharacters so the result matches the original text literally when passed to regex-based built-ins such as `REPLACE` or `STRCOUNT`.

**Errors & validation**
- None.

**Examples**
- `ESCAPE("a+b")` → `"a\+b"`

**Progress state**
- complete
