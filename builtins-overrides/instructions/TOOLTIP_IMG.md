**Summary**
- Enables/disables “image tooltip” interpretation in custom-draw tooltips.

**Tags**
- ui

**Syntax**
- `TOOLTIP_IMG <enabled>`

**Arguments**
- `<enabled>` (int): `0` disables; non-zero enables.

**Semantics**
- When enabled and tooltips are custom-drawn (`TOOLTIP_CUSTOM 1`):
  - If the tooltip text can be parsed as an integer `i`, the engine uses graphics resource `G:i` as the primary tooltip content.
  - If the graphics resource is not available, it falls back to drawing the tooltip text.
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_CUSTOM 1`
- `TOOLTIP_IMG 1`

**Progress state**
- complete
