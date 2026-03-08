**Summary**
- Requests an integer input from the user and stores it into `RESULT`; when `<mouse> != 0` and completion occurs via a mouse click, the UI also writes mouse-side-channel metadata.

**Tags**
- io

**Syntax**
- `INPUT [<default> [, <mouse> [, <canSkip> [, <extra>]]]]`

**Arguments**
- `<default>` (optional, int): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** also submits its value as `INPUT` even when this argument is omitted or `0`.
  - If non-zero, the UI additionally writes the mouse side-channel metadata described below.
  - `0`: accepted integer values on the normal completion path are written to `RESULT`.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- `<extra>` (optional, int): accepted by the argument parser but ignored by the runtime (not read/evaluated).

**Semantics**
- Enters an integer-input UI wait.
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input value on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- `INPUT` itself does not start a timed wait; use `TINPUT` / `TINPUTS` for timed waits. While a timed wait is active, the shared console input layer can suppress the usual “empty input uses default” path.
- On successful completion:
  - Writes the accepted integer to `RESULT`.
  - Echoes the accepted input text to output.
    - If the user submits an empty input and a default is used, the echoed text is the default’s decimal string form (e.g. `10`).
- Empty / invalid input handling:
  - If there is no default and the user submits an empty input, the input is rejected and the engine stays in the wait state.
  - If the submitted text is not a valid integer, the input is rejected and the engine stays in the wait state.
  - On a rejected input, no `RESULT*` variables are assigned and the rejected text is not echoed.
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path:
    - `<mouse>` must be present (it is read to choose the output slot).
    - `<default>` must be present; otherwise the engine throws a runtime error.
    - The accepted value is written to:
      - `RESULT` if `<mouse> == 0`
      - `RESULT_ARRAY[1]` if `<mouse> != 0`
    - The input string is not echoed (because the UI wait is skipped entirely).
- Mouse side channels (UI behavior when `<mouse> != 0`):
  - If the instruction requested mouse side-channel mode and the user completes input via a mouse click, the UI also writes metadata into:
    - `RESULT_ARRAY[1]`: mouse button (`1`=left, `2`=right, `3`=middle).
    - `RESULT_ARRAY[2]`: a modifier-key bitfield (Shift=`2^16`, Ctrl=`2^17`, Alt=`2^18`).
    - `RESULTS_ARRAY[1]`: the clicked button’s string (if any).
    - `RESULT_ARRAY[3]`: mapped “button color” (see below).
  - These side channels are only written on the UI click completion path (not on keyboard-only completion, and not in the `MesSkip` no-wait path).

#### Mapped “button color” (`RESULT:3`) from `<img srcm='...'>`

When a click completes input **and** `<mouse> != 0`, the UI computes `RESULT:3` as follows:

- If the clicked button contains at least one HTML `<img ...>` segment, take the **last** `<img ...>` in that button.
- If that `<img>` has a `srcm` mapping sprite that exists and is loaded:
  - Convert the click position to a pixel coordinate in the mapping sprite by scaling within the rendered image rectangle:
    - Let `drawnWidthPx` / `drawnHeightPx` be the (positive) rendered size of that `<img>` segment.
    - Let `localX` / `localY` be the click position inside that rendered rectangle, in pixels.
    - Let `mapWidthPx` / `mapHeightPx` be the mapping sprite’s base size, in pixels.
    - The sampled mapping coordinate uses integer division (floor):
      - `mapX = localX * mapWidthPx / drawnWidthPx`
      - `mapY = localY * mapHeightPx / drawnHeightPx`
  - Sample the mapping sprite pixel color at `(mapX, mapY)`.
  - Store `RESULT:3 = (color.ToArgb() & 0x00FFFFFF)` (24-bit RGB).
- Otherwise, store `RESULT:3 = 0`.

Compatibility notes:

- The mapping color uses the mapping sprite’s base size (the size defined by `resources/**/*.csv`), not the drawn size.
- If the click is exactly on the image rectangle boundary, the mapping color is treated as `0` (the hit-test uses strict `>`/`<`).
- Other input waits can use a different `RESULT:*` payload layout; `INPUTMOUSEKEY`, for example, does not reuse `INPUT`'s `RESULT:3` button-color slot.
- When output skipping is enabled, the engine normally skips `INPUT`.
  - Exception: if output skipping was enabled by `SKIPDISP`, reaching `INPUT` is a runtime error.

**Errors & validation**
- Argument-type errors are raised if a provided argument is not an `int` expression (including `<canSkip>` and `<extra>`).
- Integer parsing is equivalent to `.NET` `Int64.TryParse` on the submitted text.
  - If parsing fails, the engine stays in the wait state.

**Examples**
- `INPUT`
- `INPUT 0`
- `INPUT 10, 1, 1` (default=10, mouse input enabled, skip can auto-accept default)

**Progress state**
- complete
