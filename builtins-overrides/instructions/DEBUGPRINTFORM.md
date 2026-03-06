**Summary**
- Appends a FORM/formatted string result to the separate debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINTFORM`
- `DEBUGPRINTFORM <formString>`

**Arguments**
- `<formString>` (optional, default `""`): FORM/formatted string, parsed like `PRINTFORM*`.

**Semantics**
- Evaluates `<formString>` using the normal FORM/formatted-string rules, then appends the resulting string to the host's separate debug-output buffer.
- Layer boundary:
  - this does not add normal display lines,
  - `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`, `LINECOUNT`, and `OUTPUTLOG` do not read it.
- If debug mode is disabled, the formatted string is still parsed/evaluated, but the resulting text is not shown anywhere visible.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- FORM parsing/evaluation errors follow the normal `PRINTFORM*` rules.

**Examples**
```erabasic
DEBUGPRINTFORM "X={VALUE}"
```

**Progress state**
- complete
