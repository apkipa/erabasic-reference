**Summary**
- Returns the minimum integer value in an array range.

**Tags**
- arrays

**Syntax**
- `MINARRAY(arrayVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MINARRAY(arrayVarTerm)` → `long`
- `MINARRAY(arrayVarTerm, startIndex)` → `long`
- `MINARRAY(arrayVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int 1D array variable term): a 1D integer array variable term. Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `startIndex` (optional, int; default `0`): start index.
- `endIndex` (optional, int; default current array length): end index.

**Semantics**
- Reads `ret = element[startIndex]`, then scans `i` from `startIndex + 1` while `i < endIndex`, and updates `ret = min(ret, element[i])`.
- If `endIndex <= startIndex`, returns `element[startIndex]` (the single element at `startIndex`).

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not an integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= length`
  - `endIndex < 0` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `m = MINARRAY(A)`
- `m = MINARRAY(A, 10, 20)`

**Progress state**
- complete

