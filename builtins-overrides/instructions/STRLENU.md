**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a raw string argument.

**Tags**
- text

**Syntax**
- `STRLENU <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

- Omitted arguments / defaults:
  - If omitted, the string defaults to `""`.

**Semantics**
- Computes length as `str.Length` and assigns it to `RESULT`.

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLENU ABC` sets `RESULT` to `3`.

**Progress state**
- complete
