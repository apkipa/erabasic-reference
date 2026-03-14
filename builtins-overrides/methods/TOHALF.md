**Summary**
- Converts characters to half-width (narrow) form by passing the East Asian locale ID selected by config item `useLanguage` to the platform width-conversion routine.

**Tags**
- text

**Syntax**
- `TOHALF(str)`

**Signatures / argument rules**
- `TOHALF(str)` → `string`

**Arguments**
- `str` (string): input string.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise:
  - compute the derived runtime value `LanguageLCID` from config item `useLanguage` (see `config-items.md`).
  - call Visual Basic `.NET` API `Microsoft.VisualBasic.Strings.StrConv(str, Narrow, <locale id>)`, using derived runtime value `LanguageLCID` as the third argument.
- In the open-source `.NET` implementation, that `StrConv(..., Narrow, ...)` path validates the locale as Japanese/Korean/Chinese, sets `LCMAP_HALFWIDTH`, and then calls the Windows NLS mapping routine.
- The engine does not apply its own post-processing or per-character remapping after that call.
- The engine has no script-visible per-language branch here other than selecting derived runtime value `LanguageLCID` and passing it through to `StrConv`.
- Exact per-character results are whatever the platform Visual Basic / Windows `Narrow` conversion routine returns for that locale ID.
- See the note under derived runtime value `LanguageLCID` in `config-items.md` for the compatibility conclusion about locale invariance across the East Asian locales accepted here.
- This function does **not** use the derived runtime value `LanguageCodePage`; that code page is used by `LangManager` byte-length helpers instead.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exception from the underlying conversion routine propagates as an engine error.

**Examples**
- `TOHALF("ＡＢＣ１２３")` → `"ABC123"`

**Progress state**
- complete
