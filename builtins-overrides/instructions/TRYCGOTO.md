**Summary**
- Like `TRYGOTO`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCGOTO <labelName>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTO`.

**Semantics**
- If the `$label` exists: behaves like `GOTO` (jumps to the label). Whether the `CATCH` line is ever reached depends on subsequent control flow.
- If the `$label` does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).

**Examples**
- `TRYCGOTO OPTIONAL_LABEL`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`

**Progress state**
- complete
