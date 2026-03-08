**Summary**
- Joins a slice of an array into one string.

**Tags**
- text

**Syntax**
- `STRJOIN(arrayRef [, delimiter [, start [, count]]])`

**Signatures / argument rules**
- `STRJOIN(arrayRef)` → `string`
- `STRJOIN(arrayRef, delimiter)` → `string`
- `STRJOIN(arrayRef, delimiter, start)` → `string`
- `STRJOIN(arrayRef, delimiter, start, count)` → `string`

**Arguments**
- `arrayRef` (array variable reference): source array to join. May be an int or string array.
- `delimiter` (optional, string; default `","`): separator inserted between items.
- `start` (optional, int; default `0`): first index in the joined slice.
- `count` (optional, int): number of items to join. If omitted, defaults to `lastDimensionLength - start`.

**Semantics**
- `arrayRef` must be an array variable reference, not an array-valued expression.
- Works with 1D, 2D, and 3D arrays:
  - for 1D arrays, joins along that only dimension,
  - for 2D/3D arrays, joins along the **last** dimension while keeping earlier indices fixed by `arrayRef`.
- Omitted `delimiter` uses `","`; explicit `""` is distinct and joins without a separator.
- Omitted `count` is computed as `lastDimensionLength - start` before range validation.
  - If that computed value is negative, the call fails with the normal negative-`count` error.
- Range rules after defaults:
  - `count < 0` is an error,
  - `start` and `start + count` must both satisfy `0 <= value <= lastDimensionLength`.
- Return construction:
  - string-array elements are concatenated as stored,
  - int-array elements are converted with normal decimal `ToString()` before joining.
- If `count == 0`, returns `""`.

**Errors & validation**
- Runtime error if `arrayRef` is not an array variable reference.
- Runtime error if `count < 0`.
- Runtime error if the selected slice is outside the last-dimension bounds.

**Examples**
- If `ARR = ["a", "b", "c"]`, `STRJOIN(ARR, "|", 1, 2)` → `"b|c"`

**Progress state**
- complete
