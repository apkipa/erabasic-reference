**Summary**
- Builds a 24-bit RGB integer from separate color components.

**Tags**
- ui

**Syntax**
- `COLOR_FROMRGB(r, g, b)`

**Signatures / argument rules**
- `COLOR_FROMRGB(r, g, b)` → `long`

**Arguments**
- `r` (int): red component, must satisfy `0 <= r <= 255`.
- `g` (int): green component, must satisfy `0 <= g <= 255`.
- `b` (int): blue component, must satisfy `0 <= b <= 255`.

**Semantics**
- Returns `0xRRGGBB` as an integer:
  - `(r << 16) + (g << 8) + b`.

**Errors & validation**
- Runtime error if any component is outside `0..255`.

**Examples**
- `c = COLOR_FROMRGB(255, 0, 0)` returns `0xFF0000`.

**Progress state**
- complete

