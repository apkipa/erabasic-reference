**Summary**
- Appends a filled rectangle shape part to the current output line (equivalent to a `<shape type='rect' ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_RECT <width>`
- `PRINT_RECT <x>, <y>, <width>, <height>`

**Arguments**
- The numeric arguments are int expressions in mixed units:
  - A numeric argument may be followed by a `px` suffix token to indicate pixels (e.g. `30px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (pixels): `valuePx = value * FontSize / 100`.
- 1-argument form:
  - `<width>`: rectangle width (must be `> 0`).
  - Height is the current font size (pixels), and the rectangle starts at `(x=0, y=0)` within the line box.
- 4-argument form:
  - `<x>, <y>, <width>, <height>` define the rectangle (must satisfy `x >= 0`, `width > 0`, `height > 0`; `y` may be negative).

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
