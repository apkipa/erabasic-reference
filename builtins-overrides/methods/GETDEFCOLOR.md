**Summary**
- Returns the configured default foreground text color as a 24-bit RGB integer.

**Tags**
- ui
- config

**Syntax**
- `GETDEFCOLOR()`

**Signatures / argument rules**
- `GETDEFCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configured default text color (`ForeColor`) as `0xRRGGBB`:
  - `ForeColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETDEFCOLOR()`

**Progress state**
- complete

