**Summary**
- Returns the width of a created graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GWIDTH(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GWIDTH(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Returns the width of the referenced graphics surface.
- If the graphics surface is not currently created, returns `0`.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
- `W = GWIDTH(GID)`

**Progress state**
- complete
