**Summary**
- Sets `RESULT` to the engine’s length measure based on derived runtime value `LanguageCodePage` for a raw string argument.

**Tags**
- text

**Syntax**
- `STRLEN [<rawString>]`

**Arguments**
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string).


**Semantics**
- Computes length via the engine’s byte-count rule based on derived runtime value `LanguageCodePage` and assigns it to `RESULT`:
  - For ASCII-only strings: equals `str.Length`.
  - Otherwise: equals the byte count of `str` under derived runtime value `LanguageCodePage` (see `config-items.md`).
- For normal expression-style string evaluation (quotes, `%...%`, `{...}`), use `STRLENFORM` instead.

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLEN ABC` sets `RESULT` to the byte length of `ABC` under derived runtime value `LanguageCodePage`.

**Progress state**
- complete
