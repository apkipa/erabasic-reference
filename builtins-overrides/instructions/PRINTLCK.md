**Summary**
- `PRINTLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTLCK [<raw text>]`
- `PRINTLCK;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCK ...`

**Progress state**
- complete
