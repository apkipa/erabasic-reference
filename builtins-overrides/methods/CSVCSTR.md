**Summary**
- Returns a CSV-defined `CSTR` string entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVCSTR(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVCSTR(charaNo, index)` → `string`
- `CSVCSTR(charaNo, index, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `CSTR` element index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when config item `CompatiSPChara` = `YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `CSTR[index]` entry.
- If the template has no `CSTR` table, returns `""`.
- If the template has a `CSTR` table and `index` is in range but no explicit entry is defined at that slot, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - this build does not expose a stable public selector for duplicate normal/SP templates that share the same `NO`, so `spFlag` alone is not a reliable disambiguator.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `CSTR` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVCSTR(0, 2)`

**Progress state**
- complete
