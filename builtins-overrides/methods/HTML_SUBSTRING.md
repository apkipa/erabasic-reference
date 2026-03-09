**Summary**
- Splits an HTML string into a prefix that fits within a given display width and the remaining suffix.

**Tags**
- io

**Syntax**
- `HTML_SUBSTRING(html, width)`

**Signatures / argument rules**
- Signature: `string HTML_SUBSTRING(string html, int width)`.
- Also writes results into `RESULTS` (see semantics).

**Arguments**
- `html` (string): HTML string.
- `width` (int): width in half-width character units.

**Semantics**
- Returns the first part (the prefix) as an HTML string.
- Writes the split results into `RESULTS`:
  - `RESULTS:0` = returned prefix
  - `RESULTS:1` = remaining suffix (may be `""`)
  - Other `RESULTS:*` entries are not cleared.
- Interprets `width` in “half-width character units”. One unit corresponds to half the configured font size in pixels:
  - Let `fontSizePx` be config item `FontSize`; then `pixelBudget = width * fontSizePx / 2`.
- Expands character references in `html` first, then performs the split.
  - This means that sequences like `&lt;b&gt;` may become `<b>` tags after expansion and affect the split.
- If the expanded HTML contains a `<br>` tag, it forces the split at that point:
  - The prefix ends before the `<br>`.
  - The suffix starts after the `<br>`.
  - The `<br>` tag itself is not included in either result.
- Compatibility notes:
  - The special handling of `<br>`, `<img ...>`, and `<shape ...>` is case-sensitive (`br`/`img`/`shape` in lowercase). For example, `<BR>` is not treated as a forced split point.
  - Literal newline characters (`'\n'`) are not treated as forced split points by this function (unlike `HTML_PRINT` rendering).
- Treats `<img ...>` and `<shape ...>` as indivisible units when splitting:
  - If the current line already has content and the next figure would exceed the width budget, the figure is left for the suffix.
- Produces output HTML that keeps basic style tag balance across the split boundary (so the prefix and suffix remain renderable HTML strings in this mini language).

**Errors & validation**
- Invalid HTML strings (including invalid character references) may raise runtime errors.

**Examples**
```erabasic
PRINTSL HTML_SUBSTRING("AB<b>CD</b>EFG", 4)
PRINTSL RESULTS:1
```

**Progress state**
- complete
