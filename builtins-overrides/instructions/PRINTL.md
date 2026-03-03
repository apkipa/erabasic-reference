**Summary**
- `PRINTL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTL [<raw text>]`
- `PRINTL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTL ...`

**Progress state**
- complete
