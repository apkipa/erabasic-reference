**Summary**
- Sets the current fill brush of a graphics surface to a solid color.

**Tags**
- graphics

**Syntax**
- `GSETBRUSH(gID, cARGB)`

**Signatures / argument rules**
- `GSETBRUSH(gID, cARGB)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- On success replaces the current brush with a `SolidBrush` of the requested color and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB < 0` or `cARGB > 0xFFFFFFFF`.

**Examples**
- `GSETBRUSH 0, 0xFF112233`

**Progress state**
- complete
