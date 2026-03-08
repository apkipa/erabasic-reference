**Summary**
- Deletes a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_RELEASE(mapName)`

**Signatures / argument rules**
- `MAP_RELEASE(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map exists, it is removed.
- The function always returns `1`, even when the map was already absent.

**Errors & validation**
- None.

**Examples**
- `MAP_RELEASE("session")`

**Progress state**
- complete
