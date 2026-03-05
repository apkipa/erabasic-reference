**Summary**
- Sets the current font style flags (bold/italic/strikeout/underline) for subsequent text output.

**Tags**
- ui

**Syntax**
- `FONTSTYLE`
- `FONTSTYLE <flags>`

**Arguments**
- `<flags>` (optional, int; default `0`): style bit flags.
  - `1`: bold
  - `2`: italic
  - `4`: strikeout
  - `8`: underline
  - Other bits are ignored.

**Semantics**
- Computes the style as `Regular` plus any flags present in `<flags>`, then sets it as the current text style.
- Does not change the font face (see `SETFONT`).

**Errors & validation**
- (none)

**Examples**
- `FONTSTYLE 3` (bold + italic)
- `FONTSTYLE` (reset to regular)

**Progress state**
- complete
