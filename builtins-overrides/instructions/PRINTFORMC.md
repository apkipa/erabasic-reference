**Summary**
- `PRINTFORMC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMC ...`

**Progress state**
- complete
