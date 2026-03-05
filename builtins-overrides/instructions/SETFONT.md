**Summary**
- Sets the current font face name used for subsequent text output.

**Tags**
- ui

**Syntax**
- `SETFONT`
- `SETFONT <fontName>`

**Arguments**
- `<fontName>` (optional, string expression; default `""`): font face name.

**Semantics**
- If `<fontName>` is non-empty, sets the current font face name to that value.
- If `<fontName>` is empty (including when omitted), resets the current font face name to the configured default font.

**Errors & validation**
- (none)

**Examples**
- `SETFONT "MS Gothic"`
- `SETFONT` (reset to default)

**Progress state**
- complete
