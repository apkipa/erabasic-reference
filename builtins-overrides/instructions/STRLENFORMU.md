**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a FORM/formatted string.

**Tags**
- text

**Syntax**
- `STRLENFORMU [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): its evaluated result is measured.


**Semantics**
- Evaluates the formatted string to a string value, then assigns `str.Length` to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORMU NAME=%NAME%` sets `RESULT` to the character length of the expanded string.

**Progress state**
- complete
