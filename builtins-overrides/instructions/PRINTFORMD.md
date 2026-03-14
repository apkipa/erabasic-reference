**Summary**
- `PRINTFORMD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMD [<FORM string>]`

**Arguments**
- `<FORM string>` (optional, FORM/formatted string, default `""`): scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMD ...`

**Progress state**
- complete
