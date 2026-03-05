**Summary**
- Returns the maximum integer value of a character-data cell over a character-index range.

**Tags**
- characters

**Syntax**
- `MAXCARRAY(charaVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MAXCARRAY(charaVarTerm)` → `long`
- `MAXCARRAY(charaVarTerm, startIndex)` → `long`
- `MAXCARRAY(charaVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int 1D array variable term): selects which per-character cell to read.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - The subscript written after the chara selector selects the per-character cell: reads `V[i, index]`.
- `startIndex` (optional, int; default `0`): start chara index.
- `endIndex` (optional, int; default `CHARANUM`): end chara index.

**Semantics**
- Reads `ret = cell[startIndex]`, then scans `i` from `startIndex + 1` while `i < endIndex`, and updates `ret = max(ret, cell[i])`.
- If `endIndex <= startIndex`, returns `cell[startIndex]` (the single cell at `startIndex`).

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `m = MAXCARRAY(CFLAG:3)`
- `m = MAXCARRAY(CFLAG:3, 0, CHARANUM)`

**Progress state**
- complete
