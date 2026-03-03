**Summary**
- `PRINTFORMSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSK ...`

**Progress state**
- complete
