**Summary**
- Disposes a created graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GDISPOSE(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GDISPOSE(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Disposes the graphics surface currently stored at `<graphicsId>`.
- Success/failure boundary:
  - if the graphics surface is not currently created, returns `0`,
  - otherwise disposes it and returns `1`.
- After disposal, the handle may still exist conceptually, but it no longer has a created bitmap/surface.
- Layer boundary:
  - this does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
```erabasic
R = GDISPOSE(GID)
```

**Progress state**
- complete
