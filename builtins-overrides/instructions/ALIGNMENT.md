**Summary**
- Sets the horizontal alignment (left/center/right) used when the engine lays out subsequent printed lines.

**Tags**
- ui

**Syntax**
- `ALIGNMENT LEFT`
- `ALIGNMENT CENTER`
- `ALIGNMENT RIGHT`

**Arguments**
- Alignment keyword: raw token compared using the engine’s `IgnoreCase` setting.
  - This is not a string expression/literal.

**Semantics**
- Sets the current alignment for subsequent lines.

**Errors & validation**
- Runtime error if the keyword is not one of `LEFT`, `CENTER`, `RIGHT`.

**Examples**
- `ALIGNMENT CENTER`

**Progress state**
- complete
