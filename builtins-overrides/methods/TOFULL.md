**Summary**
- Converts half-width characters to full-width (wide) form using the engine’s configured language encoding (config item `useLanguage`).

**Tags**
- text

**Syntax**
- `TOFULL(str)`

**Signatures / argument rules**
- `TOFULL(str)` → `string`

**Arguments**
- `str` (string): input string.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Wide, <code page>)`, where `<code page>` is the engine’s current language code page (derived from `useLanguage`).

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOFULL("ABC")` → `"ＡＢＣ"`

**Progress state**
- complete
