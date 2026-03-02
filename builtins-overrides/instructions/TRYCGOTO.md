**Summary**
- Like `TRYGOTO`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Syntax**
- `TRYCGOTO <labelName>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTO`.

**Defaults / optional arguments**
- None.

**Semantics**
- If the `$label` exists: behaves like `GOTO`, then reaches `CATCH` sequentially and `CATCH` skips the catch body.
- If the `$label` does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Same mis-nesting warnings as other `TRYC*` constructs.

**Examples**
- `TRYCGOTO OPTIONAL_LABEL`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`
