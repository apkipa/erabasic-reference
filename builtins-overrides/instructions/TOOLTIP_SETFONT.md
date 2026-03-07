**Summary**
- Sets the font family name used when drawing tooltips (in custom-draw mode).

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETFONT <fontName>`

**Arguments**
- `<fontName>` (string): font family name.

**Semantics**
- Stores the font name used by tooltip custom drawing (`TOOLTIP_CUSTOM 1`).
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_SETFONT "MS Gothic"`

**Progress state**
- complete
