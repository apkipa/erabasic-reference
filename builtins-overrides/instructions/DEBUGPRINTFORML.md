**Summary**
- Like `DEBUGPRINTFORM`, but also appends a newline to the debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINTFORML`
- `DEBUGPRINTFORML <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): parsed like `PRINTFORM*`.

**Semantics**
- Evaluates `<formString>` using the normal FORM/formatted-string rules, appends the resulting string to the separate debug-output buffer, then appends one newline there.
- It does not affect the normal output model or any normal output readback helper.
- If debug mode is disabled, the formatted string is still parsed/evaluated, but the resulting text is not shown anywhere visible.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- FORM parsing/evaluation errors follow the normal `PRINTFORM*` rules.

**Examples**
```erabasic
DEBUGPRINTFORML "phase={PHASE}"
```

**Progress state**
- complete
