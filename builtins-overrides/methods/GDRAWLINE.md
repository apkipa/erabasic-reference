**Summary**
- Draws one straight line onto a graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GDRAWLINE(<graphicsId>, <fromX>, <fromY>, <toX>, <toY>)`

**Signatures / argument rules**
- Signature: `int GDRAWLINE(int graphicsId, int fromX, int fromY, int toX, int toY)`.
- All five arguments are evaluated as integer expressions.

**Arguments**
- `<graphicsId>` (int): target graphics-surface ID.
- `<fromX>`, `<fromY>` (int): line start point.
- `<toX>`, `<toY>` (int): line end point.

**Semantics**
- Draws a straight line from `(<fromX>, <fromY>)` to `(<toX>, <toY>)` on the target graphics surface.
- This affects only that graphics surface; it does not itself print to the console or modify the normal output model.
- Drawing state:
  - if the target graphics surface currently has an explicit drawing pen/configuration, that pen is used,
  - otherwise the line is drawn with the host's default foreground-color pen.
- Return value:
  - returns `1` when the draw operation is performed,
  - returns `0` when the target graphics object exists only as an uncreated handle/surface and therefore no drawing occurs.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if any coordinate is outside the 32-bit signed integer range.

**Examples**
```erabasic
R = GDRAWLINE(GID, 0, 0, 100, 100)
```

**Progress state**
- complete
