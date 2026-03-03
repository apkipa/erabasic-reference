**Summary**
- `PRINTFORMKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMKW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMKW ...`

**Progress state**
- complete
