**Summary**
- Timed string input: like `INPUTS`, but with a time limit and timeout message.

**Syntax**
- `TINPUTS <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<default>`: string expression; default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional): integer expression; if non-zero, displays remaining time. Default `1`.
- `<timeoutMessage>` (optional): string expression; timeout message. Default `Config.TimeupLabel`.
- `<mouse>` (optional): integer expression; enables mouse input when equal to `1` (implementation detail).
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Defaults / optional arguments**
- `<displayTime>` defaults to `1`.
- `<timeoutMessage>` defaults to `Config.TimeupLabel`.

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- `MesSkip` integration (implementation detail):
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).

**Errors & validation**
- Argument type/count errors are rejected by the argument builder.

**Examples**
- `TINPUTS 5000, "DEFAULT"`
- `TINPUTS 3000, NAME, 1, Time up!`

**Progress state**
- complete
