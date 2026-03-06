**Summary**
- Returns the ARGB color of one pixel in a sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEGETCOLOR(<spriteName>, <x>, <y>)`

**Signatures / argument rules**
- Signature: `int SPRITEGETCOLOR(string spriteName, int x, int y)`.

**Arguments**
- `<spriteName>` (string): sprite name.
- `<x>`, `<y>` (int): pixel coordinates in the sprite's base size.

**Semantics**
- If the sprite exists and the point lies inside `0 <= x < width`, `0 <= y < height`, returns that pixel's ARGB value as an unsigned 32-bit pattern carried in an integer return value.
- Returns `-1` if:
  - the sprite does not exist,
  - the sprite is not created,
  - the point is outside the sprite bounds.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.

**Examples**
```erabasic
C = SPRITEGETCOLOR("ICON", 0, 0)
```

**Progress state**
- complete
