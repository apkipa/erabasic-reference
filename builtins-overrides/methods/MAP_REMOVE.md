**Summary**
- Deletes a key from a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_REMOVE(mapName, key)`

**Signatures / argument rules**
- `MAP_REMOVE(mapName, key)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): entry key.

**Semantics**
- If the map does not exist, returns `-1`.
- Otherwise removes `key` if present and returns `1` either way.

**Errors & validation**
- None.

**Examples**
- `MAP_REMOVE("session", "token")`

**Progress state**
- complete
