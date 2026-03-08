**Summary**
- Draws a sprite resource onto a graphics surface, optionally through a color matrix.

**Tags**
- graphics
- sprites

**Syntax**
- `GDRAWSPRITE(destID, spriteName)`
- `GDRAWSPRITE(destID, spriteName, destX, destY)`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight)`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight, colorMatrix)`

**Signatures / argument rules**
- `GDRAWSPRITE(destID, spriteName)` → `long`
- `GDRAWSPRITE(destID, spriteName, destX, destY)` → `long`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight)` → `long`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight, colorMatrix)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `spriteName` (string): sprite resource name; lookup is case-insensitive.
- `destX` (optional, int): destination x coordinate.
- `destY` (optional, int): destination y coordinate.
- `destWidth` (optional, int): destination width.
- `destHeight` (optional, int): destination height.
- `colorMatrix` (optional, int 2D/3D array): 5×5 matrix source; values are divided by `256` before being passed to the color-matrix API.

**Semantics**
- If the destination graphics does not exist or has already been disposed, returns `0`.
- If the named sprite does not exist or is not created, returns `0`.
- Two-argument form draws the sprite at `(0, 0)` using the sprite's base destination size.
- Four-argument form draws at `(destX, destY)` using the sprite's base destination size.
- Six-argument form draws into the supplied destination rectangle.
- Seven-argument form behaves like the six-argument form and additionally applies the supplied color matrix.
- Rectangle parsing rejects `width == 0` and `height == 0`, but negative sizes are still forwarded as-is.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `destID` is negative or exceeds 32-bit range.
- Runtime error if any rectangle component is outside signed 32-bit range, or if any rectangle width/height is `0`.
- Runtime error if the referenced color-matrix window does not contain a full 5×5 block.

**Examples**
- `GDRAWSPRITE 0, "ICON", 10, 20`

**Progress state**
- complete
