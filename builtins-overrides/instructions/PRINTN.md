**Summary**
- `PRINTN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTN [<raw text>]`
- `PRINTN;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- `PRINTN` appends its text to the pending print buffer, then materializes the current buffered content to retained normal output, then waits for a key **without** ending the logical line.
- Observable consequence:
  - the current content becomes part of retained normal output before the wait,
  - but the next later flush is still merged into that same logical line rather than starting a new one.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped before execution.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTN ...`

**Progress state**
- complete
