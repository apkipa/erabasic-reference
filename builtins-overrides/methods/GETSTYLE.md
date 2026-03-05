**Summary**
- Returns the current text style (bold/italic/strikeout/underline) as a bitmask.

**Tags**
- ui

**Syntax**
- `GETSTYLE()`

**Signatures / argument rules**
- `GETSTYLE()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns a bitmask where:
  - bit `0` (`1`): bold
  - bit `1` (`2`): italic
  - bit `2` (`4`): strikeout
  - bit `3` (`8`): underline
- The return value is the OR of all currently enabled bits.

**Errors & validation**
- (none)

**Examples**
- `style = GETSTYLE()`

**Progress state**
- complete

