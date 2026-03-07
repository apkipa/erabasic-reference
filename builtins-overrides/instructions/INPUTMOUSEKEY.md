**Summary**
- Waits for a primitive mouse/key event (mouse down, wheel, key press, or timeout) and reports it via `RESULT` / `RESULT:*`; on the mouse-down path it may also write `RESULTS` when a selected string ordinary-output button is involved.

**Tags**
- io

**Syntax**
- `INPUTMOUSEKEY`
- `INPUTMOUSEKEY <timeMs>`

**Arguments**
- `<timeMs>` (optional, int): time limit in milliseconds.
  - If `timeMs > 0`, enables a timeout.
  - If omitted or `timeMs <= 0`, no timeout is used.

**Semantics**
- Enters a wait state for *primitive* input events (not text box submission).
- See also: `input-flow.md` (how primitive waits differ from textbox-segmentation waits) and `cbg-layer.md` (why `RESULT:4` is a separate CBG hit-map channel rather than an ordinary output-button value).
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.
- When an event occurs, the engine resumes script execution and assigns `RESULT_ARRAY[0]` through `RESULT_ARRAY[5]` (i.e. `RESULT` and `RESULT:1` through `RESULT:5`) as follows.

Event type (`RESULT`):

- `1`: mouse button down
- `2`: mouse wheel
- `3`: key press
- `4`: timeout (only possible when `timeMs > 0`)

Payload (`RESULT:*`), by event type:

- Mouse button down (`RESULT == 1`):
  - `RESULT:1`: mouse button bit flag (`MouseButtons` integer value).
    - Typical values: left=`1048576`, right=`2097152`, middle=`4194304`.
  - `RESULT:2`: mouse `x` in client pixels (origin at the left edge).
  - `RESULT:3`: mouse `y` in client pixels, using a bottom-origin coordinate: `y = rawY - ClientHeight`.
  - `RESULT:4`: current CBG button-hit-map value (24-bit RGB), or `-1` when no opaque CBG-map pixel is available at the click position.
  - `RESULT:5`: if an **integer ordinary output button** is currently selected, its button value; otherwise `0`.
  - Additionally, if a **string ordinary output button** is currently selected, the engine assigns `RESULTS = <button string>` (and `RESULT:5 = 0`).
  - No additional `RESULT:6` payload is assigned by this instruction.

- Mouse wheel (`RESULT == 2`):
  - `RESULT:1`: wheel delta.
  - `RESULT:2`: mouse `x` (same coordinate system as above).
  - `RESULT:3`: mouse `y` (same coordinate system as above).
  - `RESULT:4 = 0`, `RESULT:5 = 0`.

- Key press (`RESULT == 3`):
  - `RESULT:1`: key code (`Keys` integer value).
  - `RESULT:2`: key data (`Keys` integer value).
  - `RESULT:3 = 0`, `RESULT:4 = 0`, `RESULT:5 = 0`.

- Timeout (`RESULT == 4`):
  - `RESULT:1` through `RESULT:5` are set to `0`.

**Errors & validation**
- (none)

**Examples**
```erabasic
INPUTMOUSEKEY 1000
PRINTFORML "type=" + RESULT + " x=" + RESULT:2 + " y=" + RESULT:3
```

**Progress state**
- complete
