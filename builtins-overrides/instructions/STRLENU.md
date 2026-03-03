**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a raw string argument.

**Syntax**
- `STRLENU <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

**Defaults / optional arguments**
- If omitted, the string defaults to `""`.

**Semantics**
- Computes length as `str.Length` and assigns it to `RESULT`.

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLENU ABC` sets `RESULT` to `3`.

**Progress state**
- complete
