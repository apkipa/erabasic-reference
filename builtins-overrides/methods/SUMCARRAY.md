**Summary**
- Returns the sum of a character-data integer variable over a specified character-index range.

**Tags**
- characters
- arrays

**Syntax**
- `SUMCARRAY(charaVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `SUMCARRAY(charaVarTerm)` → `long`
- `SUMCARRAY(charaVarTerm, startIndex)` → `long`
- `SUMCARRAY(charaVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int array variable term): selects which per-character cell to read.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect which characters are scanned.
  - Subscripts written after the chara selector (if any) select which per-character cell is summed:
    - character 1D array: reads `V[i, index]`
    - character 2D array: reads `V[i, index1, 0]` (the second index is not used by this function and behaves as `0`)
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `endIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Returns `Σ charaVarTerm[i]` over character indices `i` with `startIndex <= i < endIndex` using the addressing rules above.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `sum = SUMCARRAY(CFLAG:3)`        ; sums `CFLAG[i,3]` for `0 <= i < CHARANUM`
- `sum = SUMCARRAY(TALENT:0, 0, 10)` ; sums `TALENT[i,0]` for `0 <= i < 10`

**Progress state**
- complete
