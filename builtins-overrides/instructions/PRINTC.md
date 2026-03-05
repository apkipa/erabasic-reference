**Summary**
- `PRINTC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTC [<raw text>]`
- `PRINTC;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is converted to a fixed-width “cell” string (see below).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string, and therefore produces no output.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes one fixed-width cell; does not append a newline and does not flush immediately.
- Cell formatting (right-aligned cell; observable behavior):
  - Measures string length in **Shift-JIS byte count** (hardcoded; code page 932).
  - Let `n = PrintCLength`.
  - Computes a target pixel width by measuring `n` spaces using the default font.
  - Creates a font using the current text style (font name + style) and the default font size for measurement/rendering.
    - If font creation fails, returns `str` unchanged.
  - If `len < n`, left-pads spaces to reach exactly `n` bytes.
  - It then measures the padded string’s pixel width using the created font; while the width is greater than the target width and the first character is a space, it removes one leading space and re-measures.
  - If `len >= n`, it does not add padding and does not truncate (overlong strings are kept as-is).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTC ...`

**Progress state**
- complete
