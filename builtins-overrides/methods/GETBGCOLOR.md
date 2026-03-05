**Summary**
- Returns the current background color as a 24-bit RGB integer.

**Tags**
- ui

**Syntax**
- `GETBGCOLOR()`

**Signatures / argument rules**
- `GETBGCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the current background color as `0xRRGGBB`:
  - `ConsoleBgColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETBGCOLOR()`

**Progress state**
- complete

