**Summary**
- Returns the current foreground text color as a 24-bit RGB integer.

**Tags**
- ui

**Syntax**
- `GETCOLOR()`

**Signatures / argument rules**
- `GETCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the current text color as `0xRRGGBB`:
  - `ConsoleStringColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETCOLOR()`

**Progress state**
- complete

