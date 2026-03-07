**Summary**
- Measures the display width of an HTML string (using the same layout rules as `HTML_PRINT`).

**Tags**
- io

**Syntax**
- `HTML_STRINGLEN(html [, returnPixel])`

**Signatures / argument rules**
- Signature: `int HTML_STRINGLEN(string html, int returnPixel = 0)`.
- `returnPixel` is treated as “false” only when it is exactly `0`; any non-zero value selects pixel return.

**Arguments**
- `html` (string): HTML string.
- `returnPixel` (optional, int; default `0`)
  - `0` (default): return in half-width character units.
  - non-zero: return in pixels.

**Semantics**
- Computes the rendered output for `html` using the same rules as `HTML_PRINT`.
- Measures the width of the **first display line** only (if `html` contains `<br>` or wraps, later lines do not affect the return value).
- If `returnPixel != 0`, returns the width in pixels.
- If `returnPixel = 0` (or omitted), converts pixel width to half-width character units using the configured font size:
  - Let `fontSizePx = FontSize` (see `config-items.md`).
  - Let `widthPx` be the measured pixel width (non-negative).
  - Returns the smallest integer `n` such that `n * fontSizePx / 2 >= widthPx`.
- Unless the HTML string is wrapped in `<nobr>...</nobr>`, the measured width does not exceed the drawable width (content is wrapped).

**Errors & validation**
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
PRINTFORML {HTML_STRINGLEN("<b>B</b>")}
PRINTFORML {HTML_STRINGLEN("<b>B</b>", 1)}
```

**Progress state**
- complete
