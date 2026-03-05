**Summary**
- Timed integer input: like `INPUT`, but with a time limit and timeout message.

**Tags**
- io

**Syntax**
- `TINPUT <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<default>`: integer expression; default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time (UI behavior).
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): message used on timeout.
- `<mouse>` (optional): integer expression; enables mouse input when equal to `1`.
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Semantics**
- Enters an integer-input UI wait with a timer of `<timeMs>` milliseconds (a default is always present for timed input).
- Timeout behavior:
  - When the timer expires, the engine runs the input completion path with an empty input string; this causes the default to be accepted.
  - A timeout message is displayed (either by updating the last “remaining time” line, or by printing a single line, depending on `<displayTime>`).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULT` if `<mouse> == 0`
    - `RESULT_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Output skipping interaction is the same as `INPUT`.

**Errors & validation**
- Argument parsing/type-checking errors are engine errors.

**Examples**
- `TINPUT 5000, 0`
- `TINPUT 10000, 1, 1, Time up!, 1, 1`

**Progress state**
- complete
