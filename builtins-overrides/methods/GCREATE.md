**Summary**
- Creates a graphics surface with the given size at an existing graphics ID handle.

**Tags**
- graphics
- ui

**Syntax**
- `GCREATE(<graphicsId>, <width>, <height>)`

**Signatures / argument rules**
- Signature: `int GCREATE(int graphicsId, int width, int height)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.
- `<width>` (int): surface width.
- `<height>` (int): surface height.

**Semantics**
- Creates a new graphics surface at `<graphicsId>`.
- Success/failure boundary:
  - if that graphics ID already refers to a created graphics surface, returns `0` and does nothing,
  - otherwise creates the surface and returns `1`.
- The created surface is initially blank and becomes available to later `G*` drawing operations.
- Layer boundary:
  - this does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if `<width> <= 0` or `<height> <= 0`.
- Runtime error if `<width>` or `<height>` exceeds the graphics engine's maximum supported image size.

**Examples**
```erabasic
R = GCREATE(GID, 640, 480)
```

**Progress state**
- complete
