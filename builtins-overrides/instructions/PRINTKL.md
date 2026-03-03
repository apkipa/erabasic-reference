**Summary**
- `PRINTKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTKL [<raw text>]`
- `PRINTKL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTKL ...`

**Progress state**
- complete
