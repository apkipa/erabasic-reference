**Summary**
- Requests a string input from the user and stores it into `RESULTS` (with mouse-related side channels in some cases).

**Tags**
- io

**Syntax**
- `INPUTS`
- `INPUTS <defaultFormString>`
- `INPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- `<defaultFormString>` (optional): a FORM/formatted string expression used as the default string.
- `<mouse>` (optional): integer expression; if non-zero, enables mouse-based input.
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

- Omitted arguments / defaults:
  - If `<defaultFormString>` is omitted, there is no default value.

**Semantics**
- Enters a string-input UI wait.
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
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Skip-print interaction is the same as `INPUT` (print-family skip rule + `SKIPDISP` input error case).

**Errors & validation**
- Argument parsing errors follow the underlying builder rules for `INPUTS`.
- Argument parsing quirks:
  - After the first comma, non-integer expressions are ignored with a warning.
  - Supplying `<canSkip>` may still emit a “too many arguments” warning, but the value is accepted and used by the runtime.

**Examples**
- `INPUTS`
- `INPUTS Default`
- `INPUTS Hello, %NAME%!, 1, 1`

**Progress state**
- complete
