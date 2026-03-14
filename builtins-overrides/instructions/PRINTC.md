**Summary**
- `PRINTC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTC [<raw text>]`
- `PRINTC;[<raw text>]`

**Arguments**
- `<raw text>` (optional, raw text, default `""`): raw literal text, not an expression.
- Output is padded/truncated to a fixed-width cell (config item `PrintCLength`) using hardcoded Shift-JIS byte count (code page 932, not derived runtime value `LanguageCodePage`).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTC ...`

**Progress state**
- complete
