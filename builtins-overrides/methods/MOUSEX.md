**Summary**
- Returns the current mouse X coordinate in the engine's client-coordinate system.

**Tags**
- ui
- input

**Syntax**
- `MOUSEX()`

**Signatures / argument rules**
- Signature: `int MOUSEX()`.

**Arguments**
- None.

**Semantics**
- Returns the current mouse X coordinate relative to the client area.
- If the main window does not currently exist, returns `0`.
- Coordinate convention:
  - this uses the same client-coordinate conversion used by the engine's mouse event pipeline,
  - X is measured from the left edge.

**Errors & validation**
- None.

**Examples**
- `X = MOUSEX()`

**Progress state**
- complete
