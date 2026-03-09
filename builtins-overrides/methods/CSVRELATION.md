**Summary**
- Returns the CSV-defined `RELATION` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVRELATION(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVRELATION(charaNo, index)` → `long`
- `CSVRELATION(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `RELATION` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when config item `CompatiSPChara` = `YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `RELATION[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- For `CSVRELATION`, an undefined slot returns `0`; the runtime default relation value used for live characters is **not** substituted here.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - this build does not expose a stable public selector for duplicate normal/SP templates that share the same `NO`, so `spFlag` alone is not a reliable disambiguator.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `RELATION` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVRELATION(0, 0)`

**Progress state**
- complete
