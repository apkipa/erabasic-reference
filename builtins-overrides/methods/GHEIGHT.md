**Summary**
- Returns the height of a created graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GHEIGHT(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GHEIGHT(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Returns the height of the referenced graphics surface.
- If the graphics surface is not currently created, returns `0`.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
- `H = GHEIGHT(GID)`

**Progress state**
- complete
