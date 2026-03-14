**Summary**
- `PRINTD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTD [<raw text>]`
- `PRINTD;[<raw text>]`

**Arguments**
- `<raw text>` (optional, raw text, default `""`): raw literal text, not an expression.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTD ...`

**Progress state**
- complete
