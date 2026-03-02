**Summary**
- Like `GOTO`, but if the target `$label` does not exist the instruction **does not error** and simply falls through.

**Syntax**
- `TRYGOTO <labelName>`

**Arguments**
- Same as `GOTO`.

**Defaults / optional arguments**
- None.

**Semantics**
- If the `$label` exists: behaves like `GOTO`.
- If not: does nothing (continues at the next line after `TRYGOTO`).

**Errors & validation**
- Still errors if the label exists but is invalid.

**Examples**
- `TRYGOTO OPTIONAL_LABEL`
