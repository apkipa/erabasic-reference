**Summary**
- Installs a graphics surface as the current CBG button-hit map.

**Tags**
- ui
- graphics

**Syntax**
- `CBGSETBMAPG(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int CBGSETBMAPG(int graphicsId)`.
- `<graphicsId>` is evaluated as an integer expression.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID used as the CBG hit-test map.

**Semantics**
- Selects one graphics surface as the current **CBG button-hit map**.
- The map is used for CBG mouse hit-testing by reading the pixel under the mouse:
  - if the pixel alpha is `255`, its low 24-bit RGB value becomes the selected CBG button value,
  - otherwise no CBG button is considered selected at that point.
- Layer boundary:
  - this does not add/remove normal output,
  - it only changes CBG-side hit-testing state.
- Success/failure boundary:
  - if the referenced graphics surface is not created (or has no bitmap), the method returns `0` and leaves the current hit map unchanged,
  - otherwise the method returns `1`.
- Compatibility quirk:
  - the public return value does **not** report whether the installed map is actually different from the previous one,
  - so re-setting the same already-installed map still returns `1`.
- On successful installation, current CBG hover/selection state is reset.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
```erabasic
R = CBGSETBMAPG(GID)
```

**Progress state**
- complete
