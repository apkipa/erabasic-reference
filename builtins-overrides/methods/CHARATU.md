**Summary**
- Returns the single UTF-16 code unit at a given string position.

**Tags**
- text

**Syntax**
- `CHARATU(str, position)`

**Signatures / argument rules**
- `CHARATU(str, position)` → `string`

**Arguments**
- `str` (string): source string.
- `position` (int): UTF-16 code-unit index.

**Semantics**
- If `position < 0` or `position >= str.Length`, returns `""`.
- Otherwise returns `.NET` `str[position].ToString()`.
- Indexing is by UTF-16 code unit, not Unicode scalar value.
- A supplementary character therefore occupies two positions and is **not** returned as one combined character here.

**Errors & validation**
- None.

**Examples**
- `CHARATU("ABC", 1)` → `"B"`

**Progress state**
- complete
