**Summary**
- Controls automatic repaint scheduling for the output window and can optionally force an immediate repaint.

**Tags**
- ui

**Syntax**
- `REDRAW <flags>`

**Arguments**
- `<flags>` (int): redraw flags.
  - Bit `0`:
    - `0`: disable non-forced automatic redraw (`Redraw = None`)
    - `1`: enable normal redraw (`Redraw = Normal`)
  - Bit `1`:
    - if set, forces an immediate repaint once.
  - Other bits are ignored.

**Semantics**
- Updates the console redraw mode according to bit `0`.
- If bit `1` is set, immediately repaints the current stored output state once.
- This instruction affects **paint timing**, not stored output state:
  - pending buffered output, retained normal output, and the retained HTML-island layer are not erased or rebuilt by changing redraw mode,
  - getters such as `GETDISPLAYLINE` / `HTML_GETPRINTEDSTR` still read the current stored state even if redraw is off.
- With redraw disabled:
  - non-forced repaint work is suppressed while the window is at the live bottom,
  - forced repaints still show the current stored state,
  - backlog-mode repainting is still allowed.
- The repaint applies to the whole output surface, including both the normal output area and the retained HTML-island layer.

**Errors & validation**
- None.

**Examples**
- `REDRAW 0` (stop non-forced automatic redraw)
- `REDRAW 3` (enable redraw and force an immediate repaint)

**Progress state**
- complete
