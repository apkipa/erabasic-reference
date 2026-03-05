**Summary**
- Sets the tooltip text and background colors.

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETCOLOR <foreColor>, <backColor>`

**Arguments**
- `<foreColor>` (int expression): RGB color `0x000000 .. 0xFFFFFF`.
- `<backColor>` (int expression): RGB color `0x000000 .. 0xFFFFFF`.

**Semantics**
- Updates the UI tooltip colors for subsequent tooltips.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if either color is outside `0 .. 0xFFFFFF`.

**Examples**
- `TOOLTIP_SETCOLOR 0xFFFFFF, 0x000000`

**Progress state**
- complete
