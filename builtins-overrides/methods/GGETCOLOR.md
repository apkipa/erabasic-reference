**Summary**
- Reads a single pixel from a graphics surface as unsigned ARGB.

**Tags**
- graphics

**Syntax**
- `GGETCOLOR(gID, x, y)`

**Signatures / argument rules**
- `GGETCOLOR(gID, x, y)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `x` (int): pixel x coordinate.
- `y` (int): pixel y coordinate.

**Semantics**
- Returns the pixel color as an unsigned 32-bit `0xAARRGGBB` value.
- If the target graphics does not exist or has already been disposed, returns `-1`.
- If `x < 0`, `x >= width`, or `y >= height`, returns `-1`.
- Bounds-check bug: negative `y` is not rejected by the wrapper; it falls through to the pixel API instead of returning `-1` cleanly.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error when the negative-`y` bug path reaches the underlying pixel API.

**Examples**
- `color = GGETCOLOR(0, 10, 20)`

**Progress state**
- complete
