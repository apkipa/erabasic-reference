**Summary**
- Removes a slice of elements from a mutable 1D array by shifting later elements left and filling the tail with default values.

**Tags**
- arrays

**Syntax**
- `ARRAYREMOVE <arrayVar>, <start>, <count>`

**Arguments**
- `<arrayVar>` (changeable 1D array variable term): target array.
- `<start>` (int): start index (0-based).
- `<count>` (int): number of elements to remove.

**Semantics**
- Works only on 1D arrays (int or string).
- If `<arrayVar>` is a character-data 1D array, the removal is applied to the **per-character slice** selected by `<arrayVar>`’s chara selector.
  - Any element-index subscript written after the chara selector is ignored for this instruction, but it is still evaluated once when the instruction evaluates `<arrayVar>`’s indices.
  - To target a specific character explicitly, write both indices (the element index is a dummy), e.g. `CFLAG:chara:0`.
- Removes elements in the conceptual range `[start, start+count)`:
  - Elements after the removed segment are shifted left into the gap.
  - The remaining tail is filled with defaults:
    - int arrays: `0`
    - string arrays: `null` internally (typically observed as empty string in many contexts)
- Special case: if `<count> <= 0`, the engine treats it as “remove to the end” (it effectively clears the suffix starting at `<start>`).
- If `<start> + <count>` exceeds the array length, it behaves like removing to the end.

**Errors & validation**
- Runtime errors:
  - `<start> < 0`
  - `<start> >= array length`
  - `<arrayVar>` is not a 1D array

**Examples**
- `ARRAYREMOVE A, 0, 1` (drop first element)
- `ARRAYREMOVE A, 10, -1` (clear suffix from index 10)

**Progress state**
- complete
