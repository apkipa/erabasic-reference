**Summary**
- Appends a non-drawing horizontal space part to the current output line (equivalent to a `<shape type='space' ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_SPACE <width>`

**Arguments**
- `<width>` (int expression): space width in mixed units.
  - May be followed by a `px` suffix token to indicate pixels (e.g. `40px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (pixels): `widthPx = width * FontSize / 100`.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends a space shape part to the current print buffer (no implicit newline).
- Equivalent to emitting an HTML `<shape type='space' ...>` tag; see `html-output.md` (“Shapes: `<shape ...>`”).

**Errors & validation**
- (none)

**Examples**
- `PRINT_SPACE 100` (one “em”, i.e. 100% of font size)
- `PRINT_SPACE 12px`

**Progress state**
- complete
