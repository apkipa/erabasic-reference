**Summary**
- Removes a slice of elements from a mutable 1D array by shifting later elements left and filling the tail with default values.

**Syntax**
- `ARRAYREMOVE <arrayVar>, <start>, <count>`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<start>`: integer expression; start index (0-based).
- `<count>`: integer expression; number of elements to remove.

**Defaults / optional arguments**
- None.

**Semantics**
- Works only on 1D arrays (int or string).
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
