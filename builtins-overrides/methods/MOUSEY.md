**Summary**
- Returns the current mouse Y coordinate in the engine's client-coordinate system.

**Tags**
- ui
- input

**Syntax**
- `MOUSEY()`

**Signatures / argument rules**
- Signature: `int MOUSEY()`.

**Arguments**
- None.

**Semantics**
- Returns the current mouse Y coordinate in the engine's converted client-coordinate system.
- If the main window does not currently exist, returns `0`.
- Coordinate convention:
  - this is **not** the raw top-left-based window Y,
  - it uses the engine's shared conversion `clientY - clientHeight`,
  - so values inside the client area are typically non-positive, with the bottom edge near `0`.

**Errors & validation**
- None.

**Examples**
- `Y = MOUSEY()`

**Progress state**
- complete
