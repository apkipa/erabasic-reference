**Summary**
- `PRINTFORMSW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSW <string expr>`

**Arguments**
- `<string expr>` (string): string expression whose result is then treated as a FORM/formatted string **at runtime**.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSW ...`

**Progress state**
- complete
