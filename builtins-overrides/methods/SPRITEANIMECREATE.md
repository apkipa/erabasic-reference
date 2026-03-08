**Summary**
- Creates an empty animated sprite resource.

**Tags**
- graphics
- sprites

**Syntax**
- `SPRITEANIMECREATE(spriteName, width, height)`

**Signatures / argument rules**
- `SPRITEANIMECREATE(spriteName, width, height)` → `long`

**Arguments**
- `spriteName` (string): sprite resource name; lookup is case-insensitive.
- `width` (int): animation canvas width.
- `height` (int): animation canvas height.

**Semantics**
- If `spriteName == ""`, returns `0`.
- If a sprite with that name already exists and is created, returns `0`.
- Otherwise creates an empty animated sprite canvas of the requested size and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `width <= 0` or `height <= 0`.
- Runtime error if `width` or `height` exceeds the engine image-size limit.

**Examples**
- `SPRITEANIMECREATE "WALK", 64, 64`

**Progress state**
- complete
