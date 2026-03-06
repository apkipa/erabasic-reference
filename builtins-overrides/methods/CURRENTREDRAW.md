**Summary**
- Reports whether non-forced automatic redraw is currently enabled.

**Tags**
- ui

**Syntax**
- `CURRENTREDRAW()`

**Signatures / argument rules**
- `CURRENTREDRAW()` → `long`

**Arguments**
- None.

**Semantics**
- Returns `0` if redraw mode is currently off (`REDRAW` bit `0` disabled).
- Returns `1` if redraw mode is currently on.
- This reflects only the persistent redraw mode flag.
  - It does not report whether a one-shot forced repaint just happened.
  - It does not report whether stored output state exists; redraw mode and stored output state are separate concerns.

**Errors & validation**
- None.

**Examples**
- `isRedrawing = CURRENTREDRAW()`

**Progress state**
- complete
