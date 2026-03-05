**Summary**
- Sorts a mutable 1D array in ascending or descending order, optionally within a subrange.

**Tags**
- arrays

**Syntax**
- `ARRAYSORT <arrayVar> [, FORWARD|BACK [, <start> [, <count>]]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term (int or string).
- `FORWARD|BACK` (optional; default `FORWARD`):
  - `FORWARD`: ascending
  - `BACK`: descending
- `<start>` (optional, int; default `0`): subrange start index (only parsed when `FORWARD|BACK` is present).
- `<count>` (optional, int; default “to end”): subrange length (only parsed when `FORWARD|BACK` is present). If explicitly `0`, this is a no-op.

**Semantics**
- Order defaults to ascending.
- Sorts the specified region of the array:
  - If `<count>` is omitted: sorts to end.
  - If `<count>` is provided and `<= 0`: `0` is a no-op; `<0` is an error.
- Parsing quirk:
  - `<start>` and `<count>` are only parsed when the `FORWARD|BACK` token is present.
  - If the token after the first comma is not `FORWARD` or `BACK`:
    - identifier → parse-time error
    - non-identifier (e.g. a number) → ignored (sorts the whole array with default order)

**Errors & validation**
- Parse-time errors if `<arrayVar>` is not a changeable 1D array variable term, or if the order token is present but not `FORWARD` or `BACK`.
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
