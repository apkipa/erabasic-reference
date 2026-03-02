**Summary**
- Converts half-width characters to full-width (wide) form using the engine’s configured language setting.

**Signatures / argument rules**
- `TOFULL(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Wide, Config.Language)`.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOFULL("ABC")` → `"ＡＢＣ"`
