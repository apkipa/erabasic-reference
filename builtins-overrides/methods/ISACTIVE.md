**Summary**
- Returns whether the game window is currently active.

**Tags**
- ui

**Syntax**
- `ISACTIVE()`

**Signatures / argument rules**
- `ISACTIVE()` → `long`

**Arguments**
- None.

**Semantics**
- Returns `1` if the game window is active.
- Returns `0` if it is inactive.
- This is the same window-activity state that also gates APIs such as `GETKEY*`.

**Errors & validation**
- None.

**Examples**
- `active = ISACTIVE()`

**Progress state**
- complete
