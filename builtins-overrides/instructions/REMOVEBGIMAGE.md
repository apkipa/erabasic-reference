**Summary**
- Removes one background image layer by sprite name.

**Tags**
- ui
- resources

**Syntax**
- `REMOVEBGIMAGE <spriteName>`

**Arguments**
- `<spriteName>` (FORM/formatted string): its evaluated result selects the sprite name to remove.
  - Matching is **case-sensitive** against the stored sprite name (which is uppercased during resource loading).

**Semantics**
- Removes the first background entry whose sprite name equals `<spriteName>`, then re-bakes the composite background.
- Does not print output.

**Errors & validation**
- Runtime error if no matching background entry exists.

**Examples**
- `REMOVEBGIMAGE TITLE_BG`

**Progress state**
- complete
