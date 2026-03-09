**Summary**
- Fills a rectangle on a graphics surface using the current brush.

**Tags**
- graphics

**Syntax**
- `GFILLRECTANGLE(gID, x, y, width, height)`

**Signatures / argument rules**
- `GFILLRECTANGLE(gID, x, y, width, height)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `x` (int): rectangle x coordinate.
- `y` (int): rectangle y coordinate.
- `width` (int): rectangle width.
- `height` (int): rectangle height.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- If no brush has been set with `GSETBRUSH`, fills with the current default background color from config item `BackColor`.
- Rectangle parsing rejects `width == 0` and `height == 0`, but negative sizes are still forwarded as-is.
- On success returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if any rectangle component is outside signed 32-bit range, or if `width` or `height` is `0`.

**Examples**
- `GFILLRECTANGLE 0, 10, 20, 100, 50`

**Progress state**
- complete
