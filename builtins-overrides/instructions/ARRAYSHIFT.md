**Summary**
- Shifts elements in a mutable 1D array variable by a signed offset and fills new slots with a default value.

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>`: int expression.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>`: int expression (default `0`).
- `<count>`: int expression (default “to end”; engine uses a sentinel).

**Defaults / optional arguments**
- `<start>` defaults to `0`.
- `<count>` omitted means “to the end”.

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
