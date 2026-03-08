**Summary**
- Schedules a custom textbox position/width for the next textbox-position apply point used by input waits.

**Tags**
- ui
- input

**Syntax**
- `MOVETEXTBOX(xOffset, yOffset, width)`

**Signatures / argument rules**
- `MOVETEXTBOX(xOffset, yOffset, width)` → `long`

**Arguments**
- `xOffset` (int): requested left offset.
- `yOffset` (int): requested bottom offset.
- `width` (int): requested textbox width.

**Semantics**
- Does not immediately move the textbox widget.
- Instead stores a pending textbox placement that is later applied when the host processes textbox-position changes for primitive input waits.
- Placement normalization:
  - `xOffset` is clamped so the textbox stays inside the client area with a minimum width allowance of `50`,
  - `yOffset` is interpreted from the bottom edge and clamped so the textbox stays fully visible,
  - `width` is clamped to at least `50` and at most the current host-allowed width.
- The pending position remains until it is applied or replaced.
- Returns `1`.

**Errors & validation**
- None beyond normal integer-argument evaluation.

**Examples**
- `MOVETEXTBOX(50, 30, 300)`

**Progress state**
- complete
