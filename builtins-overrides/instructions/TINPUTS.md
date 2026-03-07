**Summary**
- Timed string input: like `INPUTS`, but with a time limit and timeout message.

**Tags**
- io

**Syntax**
- `TINPUTS <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>` (int): time limit in milliseconds.
- `<default>` (string): default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time.
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): timeout message.
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** also submits its string as `TINPUTS` even when this argument is `0` or omitted.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input string on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, timed completion model, segment draining/discard rules, and `MesSkip` interaction).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse side channels when `<mouse> != 0`: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).

**Errors & validation**
- Argument parsing/type-checking errors are engine errors.

**Examples**
- `TINPUTS 5000, "DEFAULT"`
- `TINPUTS 3000, NAME, 1, Time up!`

**Progress state**
- complete
