**Summary**
- Draws one graphics surface onto another with rotation.

**Tags**
- graphics

**Syntax**
- `GDRAWGWITHROTATE(destID, srcID, angle)`
- `GDRAWGWITHROTATE(destID, srcID, angle, centerX, centerY)`

**Signatures / argument rules**
- `GDRAWGWITHROTATE(destID, srcID, angle)` → `long`
- `GDRAWGWITHROTATE(destID, srcID, angle, centerX, centerY)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `srcID` (int): source graphics id.
- `angle` (int): clockwise rotation angle in degrees.
- `centerX` (optional, int): rotation-center x coordinate.
- `centerY` (optional, int): rotation-center y coordinate.

**Semantics**
- If either graphics surface does not exist or has already been disposed, returns `0`.
- Three-argument form uses the source image center `(srcWidth / 2, srcHeight / 2)` as the rotation center.
- Five-argument form uses the supplied center coordinates.
- On success draws the rotated source and returns `1`.
- Current-build quirk: the destination graphics transform is not reset afterward, so later draw calls on the same graphics observe the accumulated transform.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if either graphics id is negative or exceeds 32-bit range.
- Runtime error if `centerX` or `centerY` is outside signed 32-bit range.

**Examples**
- `GDRAWGWITHROTATE 0, 1, 90`

**Progress state**
- complete
