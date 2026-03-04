**Summary**
- `PRINTCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTCK [<raw text>]`
- `PRINTCK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCK ...`

**Progress state**
- complete
