**Summary**
- Searches a 1D array for a target and returns the first matching index.

**Tags**
- arrays

**Syntax**
- `FINDELEMENT(arrayVarTerm, target [, startIndex [, endIndex [, exact]]])`

**Signatures / argument rules**
- `FINDELEMENT(arrayVarTerm, target)` → `long`
- `FINDELEMENT(arrayVarTerm, target, startIndex)` → `long`
- `FINDELEMENT(arrayVarTerm, target, startIndex, endIndex)` → `long`
- `FINDELEMENT(arrayVarTerm, target, startIndex, endIndex, exact)` → `long`

**Arguments**
- `arrayVarTerm` (1D array variable term): a 1D variable term (int or string). Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `target`:
  - int array: int value to match
  - string array: a **regular expression pattern** (see “Semantics”)
- `startIndex` (optional, int; default `0`): inclusive start index.
- `endIndex` (optional, int; default = array length): exclusive end index.
- `exact` (optional, int; default `0`): only meaningful for string arrays.
  - `0`: regex partial match
  - non-zero: regex full-string match

**Semantics**
- If `startIndex >= endIndex`, returns `-1`.
- int array:
  - Returns the first index `i` with `startIndex <= i < endIndex` where `array[i] == target`, or `-1` if not found.
  - `exact` is accepted but has no effect.
- string array:
  - Compiles `target` as a .NET regular expression pattern.
  - Treats `null` array elements as `""` during matching.
  - If `exact != 0`, returns the first index whose string fully matches the regex.
  - Otherwise, returns the first index whose string contains a regex match.

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not a 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range
  - the regex pattern is invalid (string array case)

**Examples**
- `i = FINDELEMENT(A, 0)`
- `i = FINDELEMENT(S, \"^Alice$\", 0, 100, 1)`

**Progress state**
- complete

