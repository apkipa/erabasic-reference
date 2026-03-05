**Summary**
- Searches a 1D array for a target and returns the last matching index.

**Tags**
- arrays

**Syntax**
- `FINDLASTELEMENT(arrayVarTerm, target [, startIndex [, endIndex [, exact]]])`

**Signatures / argument rules**
- `FINDLASTELEMENT(arrayVarTerm, target)` → `long`
- `FINDLASTELEMENT(arrayVarTerm, target, startIndex)` → `long`
- `FINDLASTELEMENT(arrayVarTerm, target, startIndex, endIndex)` → `long`
- `FINDLASTELEMENT(arrayVarTerm, target, startIndex, endIndex, exact)` → `long`

**Arguments**
- Same as `FINDELEMENT`.

**Semantics**
- Same as `FINDELEMENT`, except it searches backward and returns the last matching index in `[startIndex, endIndex)`.

**Errors & validation**
- Same as `FINDELEMENT`.

**Examples**
- `i = FINDLASTELEMENT(A, 0)`
- `i = FINDLASTELEMENT(S, \"Alice\", 0, 100, 1)`  ; exact regex match

**Progress state**
- complete

