**Summary**
- Sets the current foreground (text) color.

**Tags**
- ui

**Syntax**
- `SETCOLOR rgb`
- `SETCOLOR r, g, b`

**Arguments**
- `rgb` (int): packed `0xRRGGBB` value. Only the low 24 bits are used.
- `r`, `g`, `b` (int): color components.
  - Must satisfy `0 <= component <= 255`.

**Semantics**
- One-argument form (`rgb`):
  - Extracts components:
    - `r = (rgb & 0xFF0000) >> 16`
    - `g = (rgb & 0x00FF00) >> 8`
    - `b = (rgb & 0x0000FF)`
  - Sets the current text color to `(r, g, b)`.
- Three-argument form (`r, g, b`):
  - Validates that each component is within `0 <= component <= 255`.
  - Sets the current text color to `(r, g, b)`.
- Does not print output.

**Errors & validation**
- Parse-time warning + rejection if you pass exactly 2 arguments.
- Runtime error in the three-argument form if any component is `< 0` or `> 255`.

**Examples**
- `SETCOLOR 0xFF0000`      ; red
- `SETCOLOR 255, 0, 0`     ; red

**Progress state**
- complete

