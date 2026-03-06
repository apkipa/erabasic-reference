**Summary**
- Returns whether a graphics surface currently exists at the given graphics ID.

**Tags**
- graphics
- ui

**Syntax**
- `GCREATED(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GCREATED(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Returns `1` if the referenced graphics surface is currently created.
- Returns `0` otherwise.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
- `R = GCREATED(GID)`

**Progress state**
- complete
