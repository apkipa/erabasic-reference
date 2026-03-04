**Summary**
- Like `DATA`, but the text is a FORM/formatted string (scanned at load time).

**Tags**
- data-blocks

**Syntax**
- `DATAFORM [<FORM string>]`

**Arguments**
- Optional FORM/formatted string scanned to end-of-line.

- Omitted arguments / defaults:
  - Omitted argument is treated as empty string.

**Semantics**
- Stored into the surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` data list at load time.
- When selected, evaluated to a string at runtime and printed/concatenated.
  - The FORM string is scanned at load time and stored as an expression that is evaluated later (so it can still depend on runtime variables).

**Errors & validation**
- Must appear inside a valid surrounding block; otherwise it is a load-time error (the line is marked as error).

**Examples**
```erabasic
PRINTDATA
  DATAFORM Hello, %NAME%!
ENDDATA
```

**Progress state**
- complete
