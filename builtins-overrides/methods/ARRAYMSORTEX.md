**Summary**
- Sorts one or more array variables in-place using a key array, with explicit control of sort order and the sorted prefix length.

**Tags**
- arrays

**Syntax**
- `ARRAYMSORTEX(keyArray, arrayNameList [, isAscending [, fixedLength]])`

**Signatures / argument rules**
- `ARRAYMSORTEX(keyArray, arrayNameList)` → `long`
- `ARRAYMSORTEX(keyArray, arrayNameList, isAscending)` → `long`
- `ARRAYMSORTEX(keyArray, arrayNameList, isAscending, fixedLength)` → `long`

**Arguments**
- `keyArray` (array variable term | string):
  - Either a non-character 1D array variable term (int or string), or a string that is parsed as a variable term expression.
  - Must not be `CONST`, calculated, or character-data.
- `arrayNameList` (string 1D array variable term): a string array whose elements are variable-term strings naming the arrays to permute.
  - Each element is parsed as a variable term expression at runtime.
  - Any subscripts written in those variable-term strings are ignored; the function operates on the underlying array storage.
- `isAscending` (optional, int; default `1`): sort order flag.
  - `0` = descending
  - non-zero = ascending
- `fixedLength` (optional, int; default `-1`): how many key entries to sort.
  - `-1`: sentinel-terminated mode (see Semantics)
  - `> 0`: sorts the first `min(fixedLength, length(keyArray))` entries
  - `0`: returns `0`

**Semantics**
- Resolves `keyArray` to a key list of length `n` (indexed by `0 <= i < n`):
  - int key array:
    - if `fixedLength == -1`: collects entries until the first `0`
    - else: collects exactly `min(fixedLength, length(keyArray))` entries (including `0` values)
  - string key array:
    - if `fixedLength == -1`: returns `0` if any inspected entry is `null` or empty
    - else: collects exactly `min(fixedLength, length(keyArray))` entries
- Sorts the collected key list using:
  - int keys: numeric ordering
  - string keys: `string.CompareTo` ordering (current culture)
  - direction is controlled by `isAscending`
- For each variable-term string in `arrayNameList`, resolves it to an array variable and applies the same permutation:
  - 1D arrays: permutes elements `0 .. n-1`
  - 2D arrays: permutes rows by the first index (`[row, col]`)
  - 3D arrays: permutes slabs by the first index (`[i, j, k]`)
- If any target array’s first dimension is shorter than `n`, the function returns `0`.
  - This function is not atomic: earlier arrays may already have been permuted before the failure is detected.
- Returns `1` on success.

**Errors & validation**
- Errors if:
  - `keyArray` cannot be resolved as a non-character, non-`CONST` array variable term
  - any array name in `arrayNameList` cannot be resolved to a non-character, non-`CONST` array variable term
  - any resolved array is not an array (dimension 0)
  - any resolved array is a calculated/pseudo variable

**Examples**
```erabasic
#DIM SORT_TARGETS, 3
SORT_TARGETS:0 = "A"
SORT_TARGETS:1 = "B"
SORT_TARGETS:2 = "C"
ARRAYMSORTEX(A, SORT_TARGETS, 1)
```

**Progress state**
- complete
