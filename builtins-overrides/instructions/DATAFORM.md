**Summary**
- Like `DATA`, but the text is a FORM/formatted string (scanned at load time).

**Syntax**
- `DATAFORM [<FORM string>]`

**Arguments**
- Optional FORM/formatted string scanned to end-of-line.

**Defaults / optional arguments**
- Omitted argument is treated as empty string.

**Semantics**
- Stored into the surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` data list at load time.
- When selected, evaluated to a string at runtime and printed/concatenated.

**Errors & validation**
- Must appear inside a valid surrounding block, same as `DATA`.

**Examples**
```erabasic
PRINTDATA
  DATAFORM Hello, %NAME%!
ENDDATA
```
