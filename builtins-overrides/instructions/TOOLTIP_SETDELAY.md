**Summary**
- Sets the tooltip initial delay (time between hover and tooltip popup).

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETDELAY <delayMs>`

**Arguments**
- `<delayMs>` (int expression): delay in milliseconds.
  - Omitted argument is accepted with a warning and treated as `0`.

**Semantics**
- Sets the tooltip initial delay used by the engine’s tooltip popup logic.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if `<delayMs> < 0` or `<delayMs> > 2147483647`.

**Examples**
- `TOOLTIP_SETDELAY 500`

**Progress state**
- complete
