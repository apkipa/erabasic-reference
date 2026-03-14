**Summary**
- Sets `RESULT` to the engine’s length measure based on derived runtime value `LanguageCodePage` for a FORM/formatted string.

**Tags**
- text

**Syntax**
- `STRLENFORM [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): its evaluated result is measured; supports `%...%` and `{...}`.


**Semantics**
- Evaluates the formatted string to a string value, then computes its length based on derived runtime value `LanguageCodePage` (see `STRLEN` for details).
- Assigns the result to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORM NAME=%NAME%` sets `RESULT` to the length of the expanded string.

**Progress state**
- complete
