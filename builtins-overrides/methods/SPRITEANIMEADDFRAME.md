**Summary**
- Adds one frame to an animated sprite from a rectangle inside a graphics surface.

**Tags**
- graphics
- sprites

**Syntax**
- `SPRITEANIMEADDFRAME(spriteName, gID, x, y, width, height, offsetX, offsetY, delay)`

**Signatures / argument rules**
- `SPRITEANIMEADDFRAME(spriteName, gID, x, y, width, height, offsetX, offsetY, delay)` → `long`

**Arguments**
- `spriteName` (string): target animated-sprite name; lookup is case-insensitive.
- `gID` (int): source graphics id.
- `x` (int): source-rectangle x coordinate.
- `y` (int): source-rectangle y coordinate.
- `width` (int): source-rectangle width.
- `height` (int): source-rectangle height.
- `offsetX` (int): destination offset inside the animation canvas.
- `offsetY` (int): destination offset inside the animation canvas.
- `delay` (int): frame duration in milliseconds.

**Semantics**
- If `spriteName == ""`, returns `0`.
- If no sprite exists with that name, returns `0`.
- If the sprite name resolves to a non-animation sprite, current build follows a null-path bug and errors instead of cleanly returning `0`.
- If the source graphics does not exist or has already been disposed, returns `0`.
- The source rectangle must have positive size and lie fully inside the source graphics; otherwise the function returns `0`.
- If `delay <= 0` or `delay > 2147483647`, returns `0`.
- On success appends a frame and returns `1`.
- Offset clipping quirk: the offset is not rejected when it places the frame partly or wholly outside the animation canvas. The frame is clipped to that canvas and may become visually empty while still consuming its delay time.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if any point/rectangle coordinate is outside signed 32-bit range, or if `width` or `height` is `0`.

**Examples**
- `SPRITEANIMEADDFRAME "WALK", 0, 0, 0, 32, 32, 16, 16, 100`

**Progress state**
- complete
