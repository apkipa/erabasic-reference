**Summary**
- Returns the current base Y position of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEPOSY(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEPOSY(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's current base Y position.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `Y = SPRITEPOSY("ICON")`

**Progress state**
- complete
