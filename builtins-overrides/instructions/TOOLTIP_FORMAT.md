**Summary**
- Sets the tooltip text rendering flags used by the UI text renderer (in custom-draw mode).

**Tags**
- ui

**Syntax**
- `TOOLTIP_FORMAT <flags>`

**Arguments**
- `<flags>` (int expression): bitmask passed through as `.NET` `TextFormatFlags`.

**Semantics**
- Updates the text format flags used when drawing tooltip text in custom-draw mode (`TOOLTIP_CUSTOM 1`).
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_FORMAT 0`

**Progress state**
- complete
