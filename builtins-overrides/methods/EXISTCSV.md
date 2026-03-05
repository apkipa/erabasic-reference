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
- `isSp` (optional, int; default `0`): whether to look up in the SP-character template set.
  - `0`: normal character templates
  - non-zero: SP character templates

**Semantics**
- Returns `1` if a character template exists for `charaNo` in the selected template set, otherwise returns `0`.

**Errors & validation**
- Runtime error if `isSp != 0` while the compatibility option “use SP characters” is disabled (`CompatiSPChara = false`).

**Examples**
- `ok = EXISTCSV(100)`

**Progress state**
- complete

