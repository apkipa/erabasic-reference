**Summary**
- Sets `RESULT` to the engine’s **language/encoding length** of a raw string argument.

**Syntax**
- `STRLEN <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

**Defaults / optional arguments**
- If omitted, the string defaults to `""`.

**Semantics**
- Computes length via the engine’s language-aware length counter and assigns it to `RESULT`:
  - For ASCII-only strings: equals `str.Length`.
  - Otherwise: equals the current configured encoding’s `GetByteCount(str)` (often Shift-JIS in typical setups).
- For normal expression-style string evaluation (quotes, `%...%`, `{...}`), use `STRLENFORM` instead.

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLEN ABC` sets `RESULT` to the byte length of `ABC` under the current encoding.

**Progress state**
- complete
