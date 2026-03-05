**Summary**
- Shifts elements in a mutable 1D array variable by a signed offset and fills new slots with a default value.

**Tags**
- arrays

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>`: int (signed). `0` is a no-op.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>` (optional, int; default `0`): start index of the shifted segment.
- `<count>` (optional, int; default “to end”): number of elements in the segment. If explicitly `0`, this is a no-op.

**Semantics**
- Operates on the segment `[start, start+count)` (or `[start, end)` if count omitted).
- If `shift == 0`, does nothing.
- If shifting removes all overlap, fills the whole segment with `<default>`.
- If `start + count` exceeds array length, the engine clamps `count` to fit.

**Errors & validation**
- Errors if `<arrayVar>` is not 1D, if `start < 0`, if `count < 0` (when provided), or if `start >= arrayLength`.

**Examples**
- `ARRAYSHIFT SOME_INT_ARRAY, 1, 0`
- `ARRAYSHIFT SOME_STR_ARRAY, -2, "", 10`

**Progress state**
- complete
