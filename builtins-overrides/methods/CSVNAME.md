**Summary**
- Returns the CSV-defined `NAME` string for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVNAME(charaNo [, spFlag])`

**Signatures / argument rules**
- `CSVNAME(charaNo)` → `string`
- `CSVNAME(charaNo, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read from the CSV-backed character-template database.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its CSV-defined `NAME` string.
- If that field is absent or `null` in the template, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - this build does not expose a stable public selector for duplicate normal/SP templates that share the same `NO`, so `spFlag` alone is not a reliable disambiguator.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVNAME(0)`

**Progress state**
- complete
