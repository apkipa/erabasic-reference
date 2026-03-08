**Summary**
- Draws one graphics surface onto another, optionally through a color matrix.

**Tags**
- graphics

**Syntax**
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight)`
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight, colorMatrix)`

**Signatures / argument rules**
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight)` → `long`
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight, colorMatrix)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `srcID` (int): source graphics id.
- `destX` (int): destination rectangle x coordinate.
- `destY` (int): destination rectangle y coordinate.
- `destWidth` (int): destination rectangle width.
- `destHeight` (int): destination rectangle height.
- `srcX` (int): source rectangle x coordinate.
- `srcY` (int): source rectangle y coordinate.
- `srcWidth` (int): source rectangle width.
- `srcHeight` (int): source rectangle height.
- `colorMatrix` (optional, int 2D/3D array): 5×5 matrix source; values are divided by `256` before being passed to the color-matrix API.

**Semantics**
- If either graphics surface does not exist or has already been disposed, returns `0`.
- Otherwise draws the selected source rectangle into the selected destination rectangle and returns `1`.
- Source and destination may be the same graphics surface.
- Rectangle parsing rejects `width == 0` and `height == 0`, but negative sizes are still forwarded as-is.
- Color-matrix lookup rules: for 2D arrays, reads a 5×5 block starting at the referenced indices; for 3D arrays, fixes the first index and reads a 5×5 block from the second / third indices.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if any graphics id is negative or exceeds 32-bit range.
- Runtime error if any rectangle component is outside signed 32-bit range, or if any rectangle width/height is `0`.
- Runtime error if the referenced color-matrix window does not contain a full 5×5 block.

**Examples**
- `GDRAWG 0, 1, 0, 0, 100, 100, 0, 0, 100, 100`

**Progress state**
- complete
