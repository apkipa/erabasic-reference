**Summary**
- Shifts elements in a mutable 1D array variable by an offset (can be negative) and fills new slots with a default value.

**Tags**
- arrays

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>` (int): shift offset (can be negative). `0` is a no-op.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>` (optional, int; default `0`): start index of the shifted segment.
- `<count>` (optional, int; default “to end”): number of elements in the segment. If explicitly `0`, this is a no-op.

**Semantics**
- If `<arrayVar>` is a character-data 1D array, the shift is applied to the **per-character slice** selected by `<arrayVar>`’s chara selector.
  - Any element-index subscript written after the chara selector is ignored for this instruction, but it is still evaluated once when the instruction evaluates `<arrayVar>`’s indices.
  - To target a specific character explicitly, write both indices (the element index is a dummy), e.g. `CFLAG:chara:0`.
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
