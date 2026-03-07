**Summary**
- Returns the sum of elements in an integer array over a specified index range.

**Tags**
- arrays

**Syntax**
- `SUMARRAY(arrayVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `SUMARRAY(arrayVarTerm)` → `long`
- `SUMARRAY(arrayVarTerm, startIndex)` → `long`
- `SUMARRAY(arrayVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int array variable term): an integer array variable term (1D/2D/3D; character-data arrays are allowed).
  - The operation sums along the **last** dimension.
  - Any subscript written in the **last** slot of `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
    - 1D: `A:x` → sums `A[i]` (the written `x` is ignored)
    - 2D: `A:x:y` → sums `A[x, i]` (the written `y` is ignored)
    - 3D: `A:x:y:z` → sums `A[x, y, i]` (the written `z` is ignored)
    - character-data 1D: `C:chara:x` → sums `C[chara, i]` (the written `x` is ignored)
    - character-data 2D: `C:chara:x:y` → sums `C[chara, x, i]` (the written `y` is ignored)
- `startIndex` (optional, int; default `0`): inclusive start index in the summed dimension.
- `endIndex` (optional, int; default current length of the summed dimension): exclusive end index in the summed dimension.

**Semantics**
- Returns `Σ arrayVarTerm[...]` over indices `i` with `startIndex <= i < endIndex` using the addressing rules above.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not a non-`CONST` integer array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length` (where `length` is the length of the summed dimension)
  - any fixed indices inside `arrayVarTerm` are out of range
  - the ignored “last-slot” subscript written in `arrayVarTerm` is out of range

**Examples**
- `total = SUMARRAY(A, 0, 10)`
- `total = SUMARRAY(B:2:0, 5, 8)`  ; sums `B[2,5] + B[2,6] + B[2,7]`
- `total = SUMARRAY(CFLAG, 0, 100)` ; sums `CFLAG[TARGET,i]` for `0 <= i < 100`

**Progress state**
- complete
