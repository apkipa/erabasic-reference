**Summary**
- Returns the value stored for a key in a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_GET(mapName, key)`

**Signatures / argument rules**
- `MAP_GET(mapName, key)` → `string`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): lookup key.

**Semantics**
- If the map exists and contains `key`, returns the stored string value.
- If the map does not exist or the key is absent, returns `""`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORM %MAP_GET("session", "token")%`

**Progress state**
- complete
