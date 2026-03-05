**Summary**
- Controls the console redraw mode and optionally forces an immediate redraw.

**Tags**
- ui

**Syntax**
- `REDRAW <flags>`

**Arguments**
- `<flags>` (int expression): redraw flags.
  - Bit `0`:
    - `0`: disable automatic redraw (`Redraw = None`)
    - `1`: enable normal redraw (`Redraw = Normal`)
  - Bit `1`:
    - if set, forces an immediate redraw once (`RefreshStrings(true)`).
  - Other bits are ignored.

**Semantics**
- Updates the console’s redraw mode according to `<flags>`.

**Errors & validation**
- (none)

**Examples**
- `REDRAW 0` (stop automatic redraw)
- `REDRAW 3` (enable redraw + force immediate refresh)

**Progress state**
- complete
