**Summary**
- Enumerates the keys stored in a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_GETKEYS(mapName)`
- `MAP_GETKEYS(mapName, doOutput)`
- `MAP_GETKEYS(mapName, outputArray, doOutput)`

**Signatures / argument rules**
- `MAP_GETKEYS(mapName)` → `string`
- `MAP_GETKEYS(mapName, doOutput)` → `string`
- `MAP_GETKEYS(mapName, outputArray, doOutput)` → `string`

**Arguments**
- `mapName` (string): map identifier.
- `doOutput` (optional, int; default `0`): non-zero enables array output in the two- and three-argument forms.
- `outputArray` (optional, string[]): destination array for copied keys.

**Semantics**
- If the map does not exist, returns `""` and does not write any outputs.
- One-argument form returns a comma-joined key list with no escaping. Keys containing commas therefore make the returned string ambiguous.
- Two-argument form with `doOutput == 0` returns `""` and writes nothing.
- Two-argument form with `doOutput != 0` copies keys to `RESULTS` starting at index `0`, sets `RESULT` to the total key count, and returns the scalar `RESULTS` value (`RESULTS:0`, meaning the first copied key or `""`).
- Three-argument form with `doOutput == 0` returns `""` and writes nothing.
- Three-argument form with `doOutput != 0` copies keys to `outputArray` starting at index `0`, sets `RESULT` to the total key count, and returns `""`.
- Copies keys starting at index `0` until the destination fills. Excess keys are ignored; untouched slots are not cleared. Enumeration order is not sorted.

**Errors & validation**
- None.

**Examples**
- `MAP_GETKEYS("session", 1)`

**Progress state**
- complete
