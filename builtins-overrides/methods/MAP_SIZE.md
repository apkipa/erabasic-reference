**Summary**
- Returns the entry count of a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_SIZE(mapName)`

**Signatures / argument rules**
- `MAP_SIZE(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map exists, returns its current entry count.
- If the map does not exist, returns `-1`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {MAP_SIZE("session")}`

**Progress state**
- complete
