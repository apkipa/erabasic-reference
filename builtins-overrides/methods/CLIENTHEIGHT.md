**Summary**
- Returns the current height of the game client's drawable picture-box area, in pixels.

**Tags**
- ui

**Syntax**
- `CLIENTHEIGHT()`

**Signatures / argument rules**
- `CLIENTHEIGHT()` → `long`

**Arguments**
- None.

**Semantics**
- Returns the live height of the current main client drawing surface in pixels.
- This is a runtime UI measurement, not a saved config value.
- The result can change while the program is running if the window/client area is resized.

**Errors & validation**
- None.

**Examples**
- `h = CLIENTHEIGHT()`

**Progress state**
- complete
