**Summary**
- Returns the length of a string in the engine's language-length unit (the same unit used by `STRLEN`, `SUBSTRING`, and `STRFIND`).

**Tags**
- text

**Syntax**
- `STRLENS(str)`

**Signatures / argument rules**
- `STRLENS(str)` → `long`

**Arguments**
- `str` (string): input string.

**Semantics**
- Returns the same count that command-form `STRLEN` would write to `RESULT`.
- The count is measured under the engine's configured language encoding:
  - ASCII-only text counts as `str.Length`.
  - Non-ASCII text counts by encoded byte length.
- This is **not** Unicode-scalar counting; the result depends on the active language encoding.

**Errors & validation**
- None.

**Examples**
- `STRLENS("ABC")` → `3`

**Progress state**
- complete
