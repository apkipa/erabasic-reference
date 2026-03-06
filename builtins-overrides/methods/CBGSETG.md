**Summary**
- Adds a graphics surface to the CBG layer at a given position and depth.

**Tags**
- ui
- graphics

**Syntax**
- `CBGSETG(<graphicsId>, <x>, <y>, <zDepth>)`

**Signatures / argument rules**
- Signature: `int CBGSETG(int graphicsId, int x, int y, int zDepth)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.

**Semantics**
- Wraps the referenced graphics surface as a CBG image entry and adds it to the client-background layer at `(<x>, <y>, zDepth)`.
- The registered entry holds a **live reference** to that graphics surface rather than a copied pixel snapshot.
  - Later drawing/mutation of the same `G` surface changes later CBG rendering for this entry.
  - Removing the CBG entry breaks that reference, but does **not** dispose the underlying graphics surface.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Success/failure boundary:
  - if the referenced graphics surface is not created or has no bitmap, returns `0` and does not add an entry,
  - otherwise returns `1` after adding the entry.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETG(GID, 0, 0, 10)
```

**Progress state**
- complete
