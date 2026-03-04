**Summary**
- Sorts a mutable 1D array in ascending or descending order, optionally within a subrange.

**Tags**
- arrays

**Syntax**
- Minimal form:
  - `ARRAYSORT <arrayVar>`
- With explicit order (required for subrange arguments):
  - `ARRAYSORT <arrayVar>, FORWARD|BACK [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term (int or string).
- `FORWARD|BACK`:
  - `FORWARD`: ascending
  - `BACK`: descending
- `<start>` (optional): integer expression; default `0`.
- `<count>` (optional): integer expression; if omitted, sorts to end.

- Omitted arguments / defaults:
  - If `FORWARD|BACK` is omitted, order defaults to ascending and the engine does not accept `<start>/<count>` (parsing quirk).
  - `<start>` defaults to `0` when `FORWARD|BACK` is present but no subrange is provided.
  - `<count>` omitted means “to the end”.

**Semantics**
- Sorts the specified region of the array:
  - The runtime treats `count <= 0` as “to the end” (but an explicitly provided `count == 0` is handled as a no-op in the instruction dispatcher).
- Parsing rule:
  - `<start>` and `<count>` are only accepted when the `FORWARD|BACK` token is present.

**Errors & validation**
- Parse-time errors if:
  - `<arrayVar>` is not a changeable 1D array variable term
  - the order token is present but not `FORWARD` or `BACK`
  - `<start>/<count>` are provided but are not integers
- Runtime errors if:
  - `<start> < 0`
  - `<start> >= array length`
  - `<start> + <count>` exceeds array length (when `<count>` is provided and positive)

**Examples**
- `ARRAYSORT A`
- `ARRAYSORT A, BACK`
- `ARRAYSORT A, FORWARD, 10, 20` (sort subrange)

**Progress state**
- complete
