**Summary**
- Converts half-width characters to full-width (wide) form using the engine’s configured language setting.

**Syntax**
- `TOFULL(str)`

**Signatures / argument rules**
- `TOFULL(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Wide, Config.Language)`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOFULL("ABC")` → `"ＡＢＣ"`

**Progress state**
- complete
