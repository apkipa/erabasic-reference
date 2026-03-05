**Summary**
- Converts a named color to a 24-bit RGB integer.

**Tags**
- ui

**Syntax**
- `COLOR_FROMNAME(name)`

**Signatures / argument rules**
- `COLOR_FROMNAME(name)` → `long`

**Arguments**
- `name` (string): a color name recognized by `System.Drawing.Color.FromName`.

**Semantics**
- If `name` resolves to a non-transparent color, returns `0xRRGGBB` as an integer:
  - `(R << 16) + (G << 8) + B`.
- If `name` is not a valid color name, returns `-1`.

**Errors & validation**
- Runtime error if `name` is `"transparent"` (case-insensitive). This special name is treated as “unsupported”.

**Examples**
- `c = COLOR_FROMNAME("Red")` returns `0xFF0000`.
- `c = COLOR_FROMNAME("not_a_color")` returns `-1`.

**Progress state**
- complete

