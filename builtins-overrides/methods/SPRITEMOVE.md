**Summary**
- Offsets the base position of a created sprite by a relative amount.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEMOVE(<spriteName>, <dx>, <dy>)`

**Signatures / argument rules**
- Signature: `int SPRITEMOVE(string spriteName, int dx, int dy)`.

**Arguments**
- `<spriteName>` (string): sprite name.
- `<dx>`, `<dy>` (int): relative offset.

**Semantics**
- If a created sprite exists under `<spriteName>`, offsets its current base position by `(<dx>, <dy>)` and returns `1`.
- If no created sprite exists under that name, returns `0` and does nothing.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - this changes later rendering of that sprite,
  - but does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if `<dx>` or `<dy>` is outside the 32-bit signed integer range.

**Examples**
```erabasic
R = SPRITEMOVE("ICON", 8, -4)
```

**Progress state**
- complete
