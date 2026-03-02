**Summary**
- Converts full-width characters to half-width (narrow) form using the engine’s configured language setting.

**Signatures / argument rules**
- `TOHALF(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Narrow, Config.Language)`.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOHALF("ＡＢＣ")` → `"ABC"`
