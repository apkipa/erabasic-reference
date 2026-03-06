**Summary**
- Requests a string input from the user and stores it into `RESULTS`; when `<mouse> != 0` and completion occurs via a mouse click, the UI also writes mouse-side-channel metadata.

**Tags**
- io

**Syntax**
- `INPUTS`
- `INPUTS <defaultFormString>`
- `INPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- `<defaultFormString>` (optional): FORM/formatted string expression used as the default string. If omitted, there is no default.
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** can still submit its string as `INPUTS` even when this argument is omitted or `0`.
- `<canSkip>` (optional, any): presence enables the `MesSkip` fast path; its value is ignored (not evaluated).

**Semantics**
- Enters a string-input UI wait.
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input string on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- If `<defaultFormString>` is provided, it is evaluated to a string and used as the default when the input is empty and the request is not running a timer.
- On successful completion:
  - Stores the string into `RESULTS`.
  - Echoes the accepted input text to output (UI behavior).
    - If the user submits an empty input and a default is used, the echoed text is that default string.
- Empty input handling:
  - If there is no default and the user submits an empty input, the accepted value is `""` (empty string).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Note: if `<canSkip>` is present, `<mouse>` must also be present (it is read in the `MesSkip` no-wait path).
- Note: if `<canSkip>` is present and `MesSkip` is true at runtime, `<defaultFormString>` must be present.
  - If it is omitted, the engine throws a runtime error when taking the `MesSkip` no-wait path.
- Mouse side channels when `<mouse> != 0`: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Output skipping interaction is the same as `INPUT`.

**Errors & validation**
- Argument parsing errors follow the underlying builder rules for `INPUTS`.
- Argument parsing quirks:
  - After the first comma, the engine tries to parse `<mouse>` as an `int` expression.
    - If it is omitted or not an integer expression, the engine warns and ignores the entire tail (mouse input is disabled; `canSkip` is not enabled).
  - Supplying `<canSkip>` may still emit a “too many arguments” warning, but its presence is accepted and used by the runtime.

**Examples**
- `INPUTS`
- `INPUTS Default`
- `INPUTS Hello, %NAME%!, 1, 1`

**Progress state**
- complete
