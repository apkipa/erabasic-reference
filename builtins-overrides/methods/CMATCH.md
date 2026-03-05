**Summary**
- Counts how many characters in the current character list have a given character-data cell equal to a target value.

**Tags**
- characters

**Syntax**
- `CMATCH(charaVarTerm, value [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `CMATCH(charaVarTerm, value)` → `long`
- `CMATCH(charaVarTerm, value, startIndex)` → `long`
- `CMATCH(charaVarTerm, value, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data variable term): selects which per-character cell to compare.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - Subscripts written after the chara selector (if any) select the per-character cell:
    - scalar character variable: compares `V[i]`
    - character 1D array: compares `V[i, index]`
    - character 2D array: compares `V[i, index1, index2]`
- `value` (int|string; must match the selected cell type): target value.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `endIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Counts character indices `i` with `startIndex <= i < endIndex` where the selected cell equals `value`.
- Equality:
  - int cell: `==`
  - string cell: `==` (ordinal string equality in .NET), with the following rule:
    - if `value` is `""`, then both `""` and `null` cells are counted as matches
- Returns the count (0 or greater).

**Errors & validation**
- Error if `charaVarTerm` is not a character-data variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `n = CMATCH(TALENT, 1)`
- `n = CMATCH(CFLAG:3, 0, 0, CHARANUM)`

**Progress state**
- complete
