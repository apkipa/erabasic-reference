**Summary**
- Returns the configured focus highlight color as a 24-bit RGB integer.

**Tags**
- ui
- config

**Syntax**
- `GETFOCUSCOLOR()`

**Signatures / argument rules**
- `GETFOCUSCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configured focus color (`FocusColor`) as `0xRRGGBB`:
  - `FocusColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETFOCUSCOLOR()`

**Progress state**
- complete

