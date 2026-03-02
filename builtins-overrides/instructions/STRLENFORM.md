**Summary**
- Sets `RESULT` to the byte-length of a FORM/formatted string under the engine’s current language/encoding rules.

**Syntax**
- `STRLENFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string expression (supports `%...%` and `{...}`).

**Defaults / optional arguments**
- If omitted, the string defaults to `""`.

**Semantics**
- Evaluates the formatted string to a string value, then computes its byte-length using the engine’s language-aware byte counter.
- Assigns the result to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORM "NAME=%NAME%"` sets `RESULT` to the byte length of the expanded string.
