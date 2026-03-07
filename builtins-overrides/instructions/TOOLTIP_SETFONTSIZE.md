**Summary**
- Sets the font size (in points) used when drawing tooltips (in custom-draw mode).

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETFONTSIZE <size>`

**Arguments**
- `<size>` (int): font size value passed to the UI font constructor.

**Semantics**
- Stores the tooltip font size used by tooltip custom drawing (`TOOLTIP_CUSTOM 1`).
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_SETFONTSIZE 12`

**Progress state**
- complete
