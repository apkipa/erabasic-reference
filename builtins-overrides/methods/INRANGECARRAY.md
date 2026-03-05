**Summary**
- Counts how many characters have a character-data cell within a numeric range.

**Tags**
- characters

**Syntax**
- `INRANGECARRAY(charaVarTerm, min, max [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `INRANGECARRAY(charaVarTerm, min, max)` → `long`
- `INRANGECARRAY(charaVarTerm, min, max, startIndex)` → `long`
- `INRANGECARRAY(charaVarTerm, min, max, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int 1D array variable term): selects which per-character cell to test.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - The subscript written after the chara selector selects the per-character cell: reads `V[i, index]`.
- `min` (int): inclusive lower bound.
- `max` (int): exclusive upper bound.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `endIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Returns how many character indices `i` satisfy:
  - `startIndex <= i < endIndex`, and
  - `min <= cell[i] < max`.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `n = INRANGECARRAY(CFLAG:3, 1, 2)` ; counts `CFLAG[i,3] == 1`

**Progress state**
- complete
