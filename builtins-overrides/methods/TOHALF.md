**Summary**
- Converts full-width characters to half-width (narrow) form using the engine’s configured language encoding (`useLanguage`).

**Tags**
- text

**Syntax**
- `TOHALF(str)`

**Signatures / argument rules**
- `TOHALF(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Narrow, <code page>)`, where `<code page>` is the engine’s current language code page (derived from `useLanguage`).

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOHALF("ＡＢＣ")` → `"ABC"`

**Progress state**
- complete
