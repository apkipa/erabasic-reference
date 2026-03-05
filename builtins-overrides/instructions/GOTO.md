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
- Compatibility parsing: after `<labelName>`, the engine also accepts an optional “call-like tail”:
  - `GOTO <labelName>(...)`
  - `GOTO <labelName>, ...`
  - These extra parts are parsed for compatibility but ignored by `GOTO`:
    - Only `<labelName>` is used to resolve the `$label`.
    - The ignored expressions are not evaluated and have no side effects (they only need to be syntactically valid).

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
- `GOTO LOOP_START(1, 2)` (equivalent to `GOTO LOOP_START`)
- `GOTO LOOP_START, 1, 2` (equivalent to `GOTO LOOP_START`)

**Progress state**
- complete
