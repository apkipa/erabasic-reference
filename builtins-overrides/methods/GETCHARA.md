**Summary**
- Returns the first registered character index in the current character list whose `NO` matches the requested character number.

**Tags**
- characters

**Syntax**
- `GETCHARA(charaNo [, spFlag])`

**Signatures / argument rules**
- `GETCHARA(charaNo)` → `long`
- `GETCHARA(charaNo, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character `NO` to search for in the current registered character list.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.

**Semantics**
- Scans the current registered character list in ascending character-index order and returns the first matching character index.
- If config item `CompatiSPChara` = `NO`:
  - `spFlag` is accepted but ignored,
  - the search matches any registered character whose `NO` equals `charaNo`.
- If `CompatiSPChara=YES`:
  - omitted / `0`: searches only non-SP registered characters,
  - non-zero: first searches non-SP registered characters; if no match is found, retries against SP registered characters.
- Returns `-1` if no matching registered character is found.

**Errors & validation**
- No special validation beyond normal integer-argument evaluation.

**Examples**
- `idx = GETCHARA(100)`
- `IF GETCHARA(100) != -1`

**Progress state**
- complete
