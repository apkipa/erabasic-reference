**Summary**
- `PRINTSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSK <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSK ...`

**Progress state**
- complete
