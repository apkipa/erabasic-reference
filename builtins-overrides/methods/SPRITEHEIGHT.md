**Summary**
- Returns the base height of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEHEIGHT(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEHEIGHT(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's base height.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `H = SPRITEHEIGHT("ICON")`

**Progress state**
- complete
