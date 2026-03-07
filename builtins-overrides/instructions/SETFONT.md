**Summary**
- Sets the current font face name used for subsequent text output.

**Tags**
- ui

**Syntax**
- `SETFONT`
- `SETFONT <fontName>`

**Arguments**
- `<fontName>` (optional, string; default `""`): font face name.

**Semantics**
- Non-empty `<fontName>` sets the current font face name.
- Empty `<fontName>` resets it to the configured default font.

**Errors & validation**
- (none)

**Examples**
- `SETFONT "MS Gothic"`
- `SETFONT` (reset to default)

**Progress state**
- complete
