**Summary**
- `PRINTN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTN [<raw text>]`
- `PRINTN;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Waits for a key **without** ending the logical output line (see `PRINT`).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTN ...`

**Progress state**
- complete
