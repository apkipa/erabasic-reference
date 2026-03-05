**Summary**
- Counts how many elements of an integer array are within a numeric range.

**Tags**
- arrays

**Syntax**
- `INRANGEARRAY(arrayVarTerm, min, max [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `INRANGEARRAY(arrayVarTerm, min, max)` → `long`
- `INRANGEARRAY(arrayVarTerm, min, max, startIndex)` → `long`
- `INRANGEARRAY(arrayVarTerm, min, max, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int 1D array variable term): a 1D integer array variable term. Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `min` (int): inclusive lower bound.
- `max` (int): exclusive upper bound.
- `startIndex` (optional, int; default `0`): inclusive start index.
- `endIndex` (optional, int; default = array length): exclusive end index.

**Semantics**
- Returns how many indices `i` satisfy:
  - `startIndex <= i < endIndex`, and
  - `min <= array[i] < max`.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not an integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `n = INRANGEARRAY(A, 0, 10)`       ; counts `0 <= A[i] < 10`
- `n = INRANGEARRAY(CFLAG, 1, 2)`   ; counts `CFLAG[TARGET,i] == 1`

**Progress state**
- complete

