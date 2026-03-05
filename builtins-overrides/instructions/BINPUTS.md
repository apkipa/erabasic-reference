**Summary**
- Like `INPUTS`, but only accepts a string that matches a currently selectable **button** on screen.

**Tags**
- io

**Syntax**
- `BINPUTS [<default> [, <mouse> [, <canSkip>]]]`

**Arguments**
- `<default>` (optional, string expression): default string used only when the submitted text is empty.
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based completion and the same mouse side channels as `INPUTS`.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).

**Semantics**
- Ensures the current output is drawn before waiting (flushes any pending buffer and forces a refresh).
- If there is no selectable button available:
  - If `<default>` is omitted: runtime error.
  - Otherwise: immediately accepts `<default>` (writes it to `RESULTS`) and returns without waiting.
- Waits for a string input and accepts it **only if** it matches a selectable button:
  - Accepted if there exists a button where either:
    - it is a string button and `buttonString == input`, or
    - it is an integer button and `buttonValue.ToString() == input`.
  - Otherwise the input is rejected and the engine stays in the wait state.
- Default handling:
  - If the user submits empty input and `<default>` is present, the engine uses the default string *as the input*.
  - That default is still rejected if no matching button exists.
- On successful completion:
  - Assigns the accepted string to `RESULTS`.
  - Echoes the accepted input text to output (UI behavior).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path:
    - `<default>` must be present; otherwise the engine throws a runtime error.
    - The accepted value is written to:
      - `RESULTS` if `<mouse> == 0`
      - `RESULTS_ARRAY[1]` if `<mouse> != 0`
    - The input string is not echoed.
- Mouse side channels:
  - When `<mouse> != 0` and the input is completed via a mouse click, the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` side channels as `INPUTS` are written (see `INPUT`).
- Output skipping (`SKIPDISP`):
  - Same interaction as `INPUTS` (runtime error).

**Errors & validation**
- Runtime error if no selectable button exists and `<default>` is omitted.
- Argument parsing quirks:
  - The parser first reads `<default>` as a formatted-string expression up to the first comma.
  - After the first comma, if `<mouse>` is omitted or is not an integer expression, the engine warns and ignores the entire tail (mouse input is disabled; `canSkip` is not enabled).
  - Supplying both `<mouse>` and `<canSkip>` may still emit a “too many arguments” warning, but the `<canSkip>` presence is accepted and used by the runtime.

**Examples**
```erabasic
PRINTBUTTONS "Yes", "Y"
PRINTBUTTONS "No", "N"
PRINTL ""
BINPUTS
PRINTFORML "picked=" + RESULTS
```

**Progress state**
- complete
