**Summary**
- Counts how many elements in an array equal a target value.

**Tags**
- arrays

**Syntax**
- `MATCH(arrayVarTerm, value [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MATCH(arrayVarTerm, value)` → `long`
- `MATCH(arrayVarTerm, value, startIndex)` → `long`
- `MATCH(arrayVarTerm, value, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (1D array variable term): a 1D variable term (int or string). Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `value` (int|string; must match the array element type): target value.
- `startIndex` (optional, int; default `0`): inclusive start index.
- `endIndex` (optional, int; default current array length): exclusive end index.

**Semantics**
- Counts indices `i` with `startIndex <= i < endIndex` where the element equals `value`.
- Equality:
  - int array: `==`
  - string array: `==` (ordinal string equality in .NET), with the following rule:
    - if `value` is `""`, then both `""` and `null` elements are counted as matches
- Returns the count (0 or greater).

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not a 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `n = MATCH(A, 0)`
- `n = MATCH(S, "", 0, 100)`
- `n = MATCH(CFLAG, 1, 0, 50)` ; counts in `CFLAG[TARGET,i]` for `0 <= i < 50`

**Progress state**
- complete
