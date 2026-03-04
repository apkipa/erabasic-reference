**Summary**
- Jumps to a local `$label` within the current function.

**Tags**
- calls

**Syntax**
- `GOTO <labelName>`

**Arguments**
- `<labelName>`: a raw string token; used to resolve a `$label` relative to the current function.

**Semantics**
- If the label exists, jumps to the `$label` marker; execution continues at the line after the `$label`.
- The argument builder accepts `(...)` / comma forms, but `GOTO` does not use argument lists; only the label name matters.

**Errors & validation**
- If the label name is a constant string and the label is missing:
  - Non-`TRY*` variants: load-time error (the line is marked as error).
  - `TRY*` variants: allowed; the instruction becomes a no-op at runtime.
- If the label name is computed at runtime (e.g. `GOTOFORM`) and the label is missing:
  - Non-`TRY*` variants: runtime error.
  - `TRY*` variants: no-op (or enters `CATCH` for `TRYC*` variants).
- Invalid label definitions are errors even for `TRY*` variants.

**Examples**
- `GOTO LOOP_START`

**Progress state**
- complete
