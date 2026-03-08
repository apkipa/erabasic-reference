**Summary**
- Checks whether a named map contains a key.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_HAS(mapName, key)`

**Signatures / argument rules**
- `MAP_HAS(mapName, key)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): lookup key.

**Semantics**
- If the map does not exist, returns `-1`.
- Otherwise returns `1` when `key` exists, or `0` when it does not.

**Errors & validation**
- None.

**Examples**
- `IF MAP_HAS("session", "token")`

**Progress state**
- complete
