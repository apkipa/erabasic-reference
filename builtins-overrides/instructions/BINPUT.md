**Summary**
- Like `INPUT`, but only accepts an integer that matches a currently selectable **integer button** on screen.

**Tags**
- io

**Syntax**
- `BINPUT [<default> [, <mouse> [, <canSkip> [, ... ]]]]`

**Arguments**
- `<default>` (optional, int expression): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button can still satisfy `BINPUT` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUT` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- Extra arguments after `<canSkip>` are accepted by the argument parser but ignored by the runtime.

**Semantics**
- Ensures the current output is drawn before waiting (flushes any pending buffer and forces a refresh).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- Selectable-button scope:
  - only buttons in the current active button generation are eligible for typed/button matching,
  - older retained buttons may remain visible in output but are not accepted once the active generation has advanced.
- If there is no selectable integer button available:
  - If `<default>` is omitted: runtime error.
  - Otherwise: immediately accepts `<default>` (writes it to `RESULT`) and returns without waiting.
- Waits for an integer input and accepts it **only if** it matches a selectable integer button value:
  - Accepted if there exists an integer button with `buttonValue == input` in the current selectable button generation.
  - Otherwise the input is rejected and the engine stays in the wait state.
- Default handling:
  - If the user submits empty input and `<default>` is present, the engine uses the default value *as the input*.
  - That default is still rejected if no matching integer button exists.
- On successful completion:
  - Assigns the accepted value to `RESULT`.
  - Echoes the accepted input text to output (UI behavior).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path:
    - `<default>` must be present; otherwise the engine throws a runtime error.
    - The accepted value is written to:
      - `RESULT` if `<mouse> == 0`
      - `RESULT_ARRAY[1]` if `<mouse> != 0`
    - The input string is not echoed.
- Mouse side channels when `<mouse> != 0`:
  - When the input is completed via a mouse click, the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` side channels as `INPUT` are written (see `INPUT`).
- Output skipping (`SKIPDISP`):
  - Same interaction as `INPUT` (reaching input while output skipping is active due to `SKIPDISP` is a runtime error).

**Errors & validation**
- Runtime error if no selectable integer button exists and `<default>` is omitted.
- Argument parsing errors if provided arguments are not integer expressions.

**Examples**
```erabasic
PRINTBUTTON "A", 10
PRINTBUTTON "B", 20
PRINTL ""
BINPUT
PRINTFORML "picked=" + RESULT
```

**Progress state**
- complete
