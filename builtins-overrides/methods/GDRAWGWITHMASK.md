**Summary**
- Draws one graphics surface onto another using a mask surface as per-pixel opacity.

**Tags**
- graphics

**Syntax**
- `GDRAWGWITHMASK(destID, srcID, maskID, destX, destY)`

**Signatures / argument rules**
- `GDRAWGWITHMASK(destID, srcID, maskID, destX, destY)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `srcID` (int): source graphics id.
- `maskID` (int): mask graphics id.
- `destX` (int): destination x coordinate.
- `destY` (int): destination y coordinate.

**Semantics**
- If any of the three graphics surfaces does not exist or has already been disposed, returns `0`.
- If `src` and `mask` sizes differ, returns `0`.
- If `destX + srcWidth > destWidth` or `destY + srcHeight > destHeight`, returns `0`.
- Otherwise uses the blue channel of the mask image as source opacity, composites onto the destination, and returns `1`.
- Negative destination coordinates are not rejected by the wrapper. They fall through to the compositor path instead of producing a clean bounds failure.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if any graphics id is negative or exceeds 32-bit range.
- Runtime error if `destX` or `destY` is outside signed 32-bit range.
- Runtime error when the negative-coordinate path reaches the underlying compositor with invalid indices.

**Examples**
- `GDRAWGWITHMASK 0, 1, 2, 10, 20`

**Progress state**
- complete
