**Summary**
- Returns the current base X position of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEPOSX(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEPOSX(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's current base X position.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `X = SPRITEPOSX("ICON")`

**Progress state**
- complete
