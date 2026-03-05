**Summary**
- Sets `RESULT` to the engine’s **language/encoding length** of a FORM/formatted string.

**Tags**
- text

**Syntax**
- `STRLENFORM [<formString>]`

**Arguments**
- `<formString>` (optional, default `""`): FORM/formatted string expression (supports `%...%` and `{...}`).


**Semantics**
- Evaluates the formatted string to a string value, then computes its language/encoding length (see `STRLEN` for details).
- Assigns the result to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORM NAME=%NAME%` sets `RESULT` to the length of the expanded string.

**Progress state**
- complete
