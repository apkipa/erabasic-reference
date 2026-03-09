**Summary**
- Appends a filled rectangle shape part to the current output line (equivalent to a `<shape type='rect' ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_RECT <width>`
- `PRINT_RECT <x>, <y>, <width>, <height>`

**Arguments**
- `<width>` (int): rectangle width in mixed units; must satisfy `width > 0`.
- `<x>` (int): 4-argument form only; rectangle X offset in mixed units and must satisfy `x >= 0`.
- `<y>` (int): 4-argument form only; rectangle Y offset in mixed units; negative values are allowed.
- `<height>` (int): 4-argument form only; rectangle height in mixed units and must satisfy `height > 0`.
- Mixed-unit rule:
  - A numeric argument may be followed by a `px` suffix token to indicate pixels (for example `30px`).
  - Without `px`, let `fontSizePx` be config item `FontSize`; then `valuePx = value * fontSizePx / 100`.
- 1-argument form defaults:
  - `x = 0`
  - `y = 0`
  - `height =` the current font size in pixels (config item `FontSize`)

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends a rectangle shape part to the current print buffer (no implicit newline).
- The shape uses the current output color as its fill color, and uses the current “button color” when selected/focused.
- The output part is equivalent to emitting an HTML `<shape type='rect' ...>` tag; see `html-output.md` (“Shapes: `<shape ...>`”) for details and the literal-text fallback behavior for invalid params.

**Errors & validation**
- Parse-time error if the number of arguments is not exactly `1` or `4`.
- If the rectangle is not drawable (unsupported parameter constraints), it is rendered as literal text (the string form of the `<shape ...>` tag).

**Examples**
- `PRINT_RECT 200` (width = 200% of font size)
- `PRINT_RECT 0px, -20px, 100px, 20px`

**Progress state**
- complete
