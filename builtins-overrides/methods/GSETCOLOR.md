**Summary**
- Writes a single pixel on a graphics surface.

**Tags**
- graphics

**Syntax**
- `GSETCOLOR(gID, cARGB, x, y)`

**Signatures / argument rules**
- `GSETCOLOR(gID, cARGB, x, y)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.
- `x` (int): pixel x coordinate.
- `y` (int): pixel y coordinate.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- If `x < 0`, `x >= width`, or `y >= height`, returns `0`.
- On success writes the pixel and returns `1`.
- Bounds-check bug: negative `y` is not rejected by the wrapper; it falls through to the pixel API instead of returning `0` cleanly.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB` is outside `0 <= value <= 0xFFFFFFFF`.
- Runtime error when the negative-`y` bug path reaches the underlying pixel API.

**Examples**
- `GSETCOLOR 0, 0xFF00FF00, 10, 20`

**Progress state**
- complete
