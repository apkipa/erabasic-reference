**Summary**
- Disposes one sprite by name.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEDISPOSE(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEDISPOSE(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- If a created sprite exists under `<spriteName>`, disposes it and returns `1`.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - disposing a sprite does not itself modify the normal output model,
  - but later rendering that depended on that sprite may stop drawing it.

**Errors & validation**
- None beyond normal string-expression evaluation.

**Examples**
```erabasic
R = SPRITEDISPOSE("ICON")
```

**Progress state**
- complete
