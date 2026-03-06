**Summary**
- Adds an existing sprite to the CBG layer at a given position and depth.

**Tags**
- ui
- graphics
- resources

**Syntax**
- `CBGSETSPRITE(<spriteName>, <x>, <y>, <zDepth>)`

**Signatures / argument rules**
- Signature: `int CBGSETSPRITE(string spriteName, int x, int y, int zDepth)`.

**Arguments**
- `<spriteName>` (string): sprite name to place on the CBG layer.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.

**Semantics**
- Looks up `<spriteName>` in the sprite table and, if it exists and is created, adds that sprite to the client-background layer at `(<x>, <y>, zDepth)`.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Success/failure boundary:
  - if the sprite does not exist or is not created, returns `0` and does not add an entry,
  - otherwise returns `1` after adding the entry.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETSPRITE("BG_ICON", 32, 16, 10)
```

**Progress state**
- complete
