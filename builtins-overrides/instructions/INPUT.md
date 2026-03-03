**Summary**
- Requests an integer input from the user and stores it into `RESULT` (with mouse-related side channels in some cases).

**Syntax**
- `INPUT`
- `INPUT <default>`
- `INPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- `<default>` (optional): integer expression for the default value.
- `<mouse>` (optional): integer expression; if non-zero, enables mouse-based input (implementation detail: selecting buttons can fill the input).
- `<canSkip>` (optional): integer expression; if present and non-zero, allows “message skip” (`MesSkip`) to auto-accept the default value without waiting.
- `<extra>` (optional): accepted by the current argument builder but ignored by the runtime implementation (implementation detail).

**Defaults / optional arguments**
- If `<default>` is omitted, there is no default value.

**Semantics**
- Enters an integer-input UI wait (`InputType.IntValue`).
- If `<default>` is provided, it becomes the default used when the input is empty and the request is not running a timer.
- On successful completion:
  - Stores the integer value into `RESULT`.
  - Echoes the entered text to output (UI behavior).
- `MesSkip` integration (implementation detail):
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULT` if `<mouse> == 0`
    - `RESULT_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels (implementation detail; WinForms UI behavior):
  - If mouse input is enabled and the user completes input via a mouse interaction, the UI may also write metadata into:
    - `RESULT_ARRAY[1]`: mouse button (`1`=left, `2`=right, `3`=middle) in some click paths.
    - `RESULT_ARRAY[2]`: a modifier-key bitfield in some click paths (Shift=`2^16`, Ctrl=`2^17`, Alt=`2^18`).
    - `RESULTS_ARRAY[1]`: the clicked button’s string (if any) in some click paths.
    - `RESULT_ARRAY[3]`: a mapped “button color” value in some click paths.
- If the script runner’s `skipPrint` mode is active (e.g. via `SKIPDISP`), `INPUT` is treated as a print-family instruction:
  - In internal skip modes, it is skipped.
  - If skip was enabled by `SKIPDISP`, reaching `INPUT` is a runtime error.

**Errors & validation**
- Argument-type errors are raised if a non-integer argument is provided.
- If input cannot be parsed as an integer, the engine stays in the wait state (no value is stored).

**Examples**
- `INPUT`
- `INPUT 0`
- `INPUT 10, 1, 1` (default=10, mouse input enabled, skip can auto-accept default)

**Progress state**
- complete
