**Summary**
- Processes pending UI events and optionally sleeps for a short time (used to yield to the UI / drive animations).

**Tags**
- ui

**Syntax**
- `AWAIT`
- `AWAIT <timeMs>`

**Arguments**
- `<timeMs>` (optional, int expression):
  - If omitted, `AWAIT` yields without sleeping.
  - Otherwise must satisfy `0 <= timeMs <= 10000`.

**Semantics**
- Forces a redraw, sets an internal “sleep” state, processes UI events, and then:
  - if `timeMs > 0`, sleeps for `timeMs` milliseconds
  - otherwise returns immediately after event processing
- Does not assign `RESULT`/`RESULTS`.
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.

**Errors & validation**
- Runtime error if `timeMs < 0` or `timeMs > 10000`.

**Examples**
- `AWAIT`         ; yield to UI
- `AWAIT 16`      ; ~60 FPS pacing

**Progress state**
- complete
