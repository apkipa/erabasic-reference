**Summary**
- Removes all entries from a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_CLEAR(mapName)`

**Signatures / argument rules**
- `MAP_CLEAR(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map exists, clears every entry and returns `1`.
- If the map does not exist, returns `-1`.

**Errors & validation**
- None.

**Examples**
- `MAP_CLEAR("session")`

**Progress state**
- complete
