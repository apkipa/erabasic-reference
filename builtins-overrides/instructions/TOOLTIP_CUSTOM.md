**Summary**
- Enables/disables owner-drawn (custom rendered) tooltips.

**Tags**
- ui

**Syntax**
- `TOOLTIP_CUSTOM <enabled>`

**Arguments**
- `<enabled>` (int expression): `0` disables custom tooltips; non-zero enables.

**Semantics**
- When enabled, tooltips are drawn via the engine’s custom draw logic, which supports:
  - custom font name/size (`TOOLTIP_SETFONT`, `TOOLTIP_SETFONTSIZE`)
  - custom text formatting flags (`TOOLTIP_FORMAT`)
  - optional image tooltips (`TOOLTIP_IMG`)
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_CUSTOM 1`

**Progress state**
- complete
