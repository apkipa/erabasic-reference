**Summary**
- Jumps to a local `$label` within the current function.

**Syntax**
- `GOTO <labelName>`

**Arguments**
- `<labelName>`: a raw string token; used to resolve a `$label` relative to the current function.

**Defaults / optional arguments**
- None.

**Semantics**
- If the label exists, jumps to the `$label` marker; execution continues at the line after the `$label`.
- The argument builder accepts `(...)` / comma forms, but `GOTO` does not use argument lists; only the label name matters.

**Errors & validation**
- Errors if the label does not exist (unless using a TRY variant) or if the label definition is invalid.

**Examples**
- `GOTO LOOP_START`
