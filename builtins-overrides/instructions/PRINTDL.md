**Summary**
- `PRINTDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTDL [<raw text>]`
- `PRINTDL;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTDL ...`

**Progress state**
- complete
