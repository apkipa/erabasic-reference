**Summary**
- Creates or replaces a sprite name by referencing a whole graphics surface or a rectangle crop from it.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITECREATE(<spriteName>, <graphicsId>)`
- `SPRITECREATE(<spriteName>, <graphicsId>, <x>, <y>, <width>, <height>)`

**Signatures / argument rules**
- `int SPRITECREATE(string spriteName, int graphicsId)`
- `int SPRITECREATE(string spriteName, int graphicsId, int x, int y, int width, int height)`

**Arguments**
- `<spriteName>` (string): sprite name to create/update.
- `<graphicsId>` (int): source graphics-surface ID.
- `<x>`, `<y>`, `<width>`, `<height>` (optional, ints): source rectangle within the graphics surface.

**Semantics**
- Creates a sprite named `<spriteName>` from the source graphics surface.
- Two-argument form:
  - uses the entire source graphics surface.
- Six-argument form:
  - uses the specified source rectangle.
- Success/failure boundary:
  - if a created sprite already exists under `<spriteName>`, returns `0` and leaves it unchanged,
  - if the source graphics surface is not created, returns `0`,
  - otherwise creates/replaces the sprite and returns `1`.
- Rectangle boundary in the six-argument form:
  - the rectangle may extend outside the source bounds,
  - but it must still intersect the source graphics area somewhere,
  - otherwise the call raises a runtime error.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - creating a sprite does not itself draw it or modify the normal output model.

**Errors & validation**
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if any rectangle coordinate/dimension argument is outside the 32-bit signed integer range.
- Runtime error if the six-argument source rectangle does not intersect the source graphics area.

**Examples**
```erabasic
R = SPRITECREATE("ICON", GID)
R = SPRITECREATE("ICON_CROP", GID, 10, 20, 64, 64)
```

**Progress state**
- complete
