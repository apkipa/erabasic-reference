**Summary**
- Like `TRYJUMP`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Syntax**
- `TRYCJUMP <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMP`.

**Defaults / optional arguments**
- Same as `JUMP`.

**Semantics**
- If the target function exists: behaves like `JUMP` (tail-call-like); the current function is discarded, so it does not return to reach `CATCH`.
- If the function does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYCJUMP OPTIONAL_PHASE`
- `CATCH`
- `  PRINTL "phase missing"`
- `ENDCATCH`

**Progress state**
- complete
