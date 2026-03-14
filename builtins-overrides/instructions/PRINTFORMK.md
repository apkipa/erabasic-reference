**Summary**
- `PRINTFORMK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMK [<FORM string>]`

**Arguments**
- `<FORM string>` (optional, FORM/formatted string, default `""`): scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMK ...`

**Progress state**
- complete
