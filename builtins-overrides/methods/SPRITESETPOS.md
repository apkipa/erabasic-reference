**Summary**
- Sets the base position of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITESETPOS(<spriteName>, <x>, <y>)`

**Signatures / argument rules**
- Signature: `int SPRITESETPOS(string spriteName, int x, int y)`.

**Arguments**
- `<spriteName>` (string): sprite name.
- `<x>`, `<y>` (int): new base position.

**Semantics**
- If a created sprite exists under `<spriteName>`, sets its base position to exactly `(<x>, <y>)` and returns `1`.
- If no created sprite exists under that name, returns `0` and does nothing.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - this changes later rendering of that sprite,
  - but does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.

**Examples**
```erabasic
R = SPRITESETPOS("ICON", 100, 50)
```

**Progress state**
- complete
