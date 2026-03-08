**Summary**
- Imports key-value pairs from XML-like text into an existing named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_FROMXML(mapName, xmlMap)`

**Signatures / argument rules**
- `MAP_FROMXML(mapName, xmlMap)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `xmlMap` (string): source text expected to contain `/map/p` entries.

**Semantics**
- If the map does not exist, returns `0`.
- Parses `xmlMap`, selects `/map/p`, and for each selected node requires exactly one `./k` child and exactly one `./v` child.
- Imported keys use `k.InnerText`; imported values use `v.InnerXml`.
- The map is not cleared first. Imported entries overwrite existing keys they mention and leave all other existing entries untouched.
- Returns `1` after successful parsing even if no usable pairs were imported.

**Errors & validation**
- Runtime error if `xmlMap` is not well-formed XML.

**Examples**
- `MAP_FROMXML("session", data)`

**Progress state**
- complete
