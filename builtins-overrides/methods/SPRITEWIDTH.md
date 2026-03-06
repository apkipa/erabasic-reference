**Summary**
- Returns the base width of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEWIDTH(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEWIDTH(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's base width.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `W = SPRITEWIDTH("ICON")`

**Progress state**
- complete
