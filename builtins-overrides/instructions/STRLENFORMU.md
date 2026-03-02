**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a FORM/formatted string.

**Syntax**
- `STRLENFORMU <formString>`

**Arguments**
- `<formString>`: FORM/formatted string expression.

**Defaults / optional arguments**
- If omitted, the string defaults to `""`.

**Semantics**
- Evaluates the formatted string to a string value, then assigns `str.Length` to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORMU "NAME=%NAME%"` sets `RESULT` to the character length of the expanded string.
