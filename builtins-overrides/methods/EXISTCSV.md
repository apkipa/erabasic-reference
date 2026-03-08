**Summary**
- Tests whether a character template exists for a given character `NO` in the CSV-backed character database.

**Tags**
- characters

**Syntax**
- `EXISTCSV(charaNo [, isSp])`

**Signatures / argument rules**
- `EXISTCSV(charaNo)` → `long`
- `EXISTCSV(charaNo, isSp)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to look up.
- `isSp` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Returns `1` if a character template exists for `charaNo`, otherwise returns `0`.
- Compatibility quirk:
  - `isSp != 0` is accepted only when `CompatiSPChara=YES`,
  - this build does not expose a stable public selector for duplicate normal/SP templates that share the same `NO`, so `isSp` alone is not a reliable disambiguator.

**Errors & validation**
- Runtime error if `isSp != 0` while the compatibility option “use SP characters” is disabled (`CompatiSPChara = false`).

**Examples**
- `ok = EXISTCSV(100)`

**Progress state**
- complete
