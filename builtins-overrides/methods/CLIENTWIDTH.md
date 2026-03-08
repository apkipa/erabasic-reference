**Summary**
- Returns the current width of the game client's drawable picture-box area, in pixels.

**Tags**
- ui

**Syntax**
- `CLIENTWIDTH()`

**Signatures / argument rules**
- `CLIENTWIDTH()` → `long`

**Arguments**
- None.

**Semantics**
- Returns the live width of the current main client drawing surface in pixels.
- This is a runtime UI measurement, not a saved config value.
- The result can change while the program is running if the window/client area is resized.

**Errors & validation**
- None.

**Examples**
- `w = CLIENTWIDTH()`

**Progress state**
- complete
