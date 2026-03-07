**Summary**
- Sorts one or more array variables in-place using the first argument as the sort key array.

**Tags**
- arrays

**Syntax**
- `ARRAYMSORT(keyArray, array1 [, array2 ...])`

**Signatures / argument rules**
- `ARRAYMSORT(keyArray, array1 [, array2 ...])` → `long`

**Arguments**
- `keyArray` (non-character 1D array variable term): sort key array; int or string; must not be `CONST` or a calculated/pseudo variable.
- `arrayN` (one or more non-character array variable terms): arrays permuted to follow the key order; each may be 1D/2D/3D and int or string; must not be `CONST` or calculated.
  - Any subscripts written in these variable terms are ignored; the function operates on the underlying array storage.

**Semantics**
- Builds a permutation by scanning `keyArray` from index `0` and collecting a prefix of entries:
  - int key array: stops at the first `0`
  - string key array: stops at the first `null` or empty string
- Sorts that collected prefix in ascending order by key:
  - int keys: numeric ascending
  - string keys: `string.CompareTo` ordering (current culture)
- Applies the resulting permutation to each argument array (including `keyArray` itself):
  - 1D arrays: permutes elements `0 <= i < n`
  - 2D arrays: permutes rows by the first index (`[row, col]`)
  - 3D arrays: permutes slabs by the first index (`[i, j, k]`)
- If any argument array’s first dimension is shorter than `n`, the function returns `0`.
  - This function is not atomic: earlier arrays may already have been permuted before the failure is detected.
- Returns `1` on success.

**Errors & validation**
- Errors if:
  - `keyArray` is not a 1D array variable term
  - any `arrayN` is not an array variable term
  - any argument is a character-data variable
  - any argument is `CONST` or a calculated/pseudo variable

**Examples**
```erabasic
ARRAYMSORT(A, B, C)
```

**Progress state**
- complete
