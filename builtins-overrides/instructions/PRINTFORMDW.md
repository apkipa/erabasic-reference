**Summary**
- `PRINTFORMDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMDW [<FORM string>]`

**Arguments**
- `<FORM string>` (optional, FORM/formatted string, default `""`): scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMDW ...`

**Progress state**
- complete
