**Summary**
- Returns the CSV-defined `EQUIP` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVEQUIP(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVEQUIP(charaNo, index)` → `long`
- `CSVEQUIP(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `EQUIP` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `EQUIP[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `EQUIP` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVEQUIP(0, 0)`

**Progress state**
- complete
