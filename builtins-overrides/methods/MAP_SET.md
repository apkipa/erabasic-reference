**Summary**
- Adds or overwrites a key-value entry in a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_SET(mapName, key, value)`

**Signatures / argument rules**
- `MAP_SET(mapName, key, value)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): entry key.
- `value` (string): stored value.

**Semantics**
- If the map does not exist, returns `-1`.
- Otherwise stores `value` under `key`, replacing any previous value, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `MAP_SET("session", "token", "abc")`

**Progress state**
- complete
