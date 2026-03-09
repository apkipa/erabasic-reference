**Summary**
- Returns the CSV-defined `BASE` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVBASE(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVBASE(charaNo, index)` → `long`
- `CSVBASE(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `BASE` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when config item `CompatiSPChara` = `YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `BASE[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- `CSVBASE` reads the template table directly; when a live character is created, the same template entries are copied into both runtime `BASE` and `MAXBASE`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - this build does not expose a stable public selector for duplicate normal/SP templates that share the same `NO`, so `spFlag` alone is not a reliable disambiguator.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `BASE` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVBASE(0, 0)`

**Progress state**
- complete
