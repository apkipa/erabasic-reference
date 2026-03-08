**Summary**
- Creates an empty named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_CREATE(mapName)`

**Signatures / argument rules**
- `MAP_CREATE(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If a map with that name already exists, returns `0` and leaves it unchanged.
- Otherwise creates an empty map and returns `1`.

**Errors & validation**
- None.

**Examples**
- `MAP_CREATE("session")`

**Progress state**
- complete
