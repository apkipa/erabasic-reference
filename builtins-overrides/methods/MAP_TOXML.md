**Summary**
- Serializes a named map to XML-like text.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_TOXML(mapName)`

**Signatures / argument rules**
- `MAP_TOXML(mapName)` → `string`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map does not exist, returns `""`.
- Otherwise returns text in the form `<map><p><k>...</k><v>...</v></p>...</map>` using the map's native enumeration order.
- Keys and values are inserted without XML escaping. Special characters such as `<`, `>`, or `&` therefore produce malformed or structurally changed output.

**Errors & validation**
- None.

**Examples**
- `data '= MAP_TOXML("session")`

**Progress state**
- complete
