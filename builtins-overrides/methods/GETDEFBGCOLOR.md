**Summary**
- Returns the configured default background color as a 24-bit RGB integer.

**Tags**
- ui
- config

**Syntax**
- `GETDEFBGCOLOR()`

**Signatures / argument rules**
- `GETDEFBGCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configured default background color (`BackColor`) as `0xRRGGBB`:
  - `BackColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETDEFBGCOLOR()`

**Progress state**
- complete

