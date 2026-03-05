**Summary**
- Resets the font style to regular (clears bold/italic/etc) for subsequent output (Windows only).

**Tags**
- ui

**Syntax**
- `FONTREGULAR`

**Arguments**
- None.

**Semantics**
- If running on Windows:
  - Sets the current font style to `Regular` (clears all style flags).
- If not running on Windows:
  - No-op.

**Errors & validation**
- (none)

**Examples**
- `FONTREGULAR`

**Progress state**
- complete

