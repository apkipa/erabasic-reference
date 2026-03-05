**Summary**
- Sets the tooltip display duration.

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETDURATION <durationMs>`

**Arguments**
- `<durationMs>` (int expression): duration in milliseconds.
  - Omitted argument is accepted with a warning and treated as `0`.

**Semantics**
- Sets how long tooltips stay visible after appearing.
  - `0` uses the UI toolkit’s default “no explicit duration” mode.
- Values greater than `32767` are clamped to `32767`.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if `<durationMs> < 0` or `<durationMs> > 2147483647`.

**Examples**
- `TOOLTIP_SETDURATION 2000`
- `TOOLTIP_SETDURATION 0` (use default/indefinite mode)

**Progress state**
- complete
