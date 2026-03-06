**Summary**
- Returns whether a created sprite currently exists under the given name.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITECREATED(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITECREATED(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns `1` if a created sprite exists under `<spriteName>`.
- Returns `0` otherwise.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `R = SPRITECREATED("ICON")`

**Progress state**
- complete
