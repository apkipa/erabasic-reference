**Summary**
- Processes pending UI events and optionally sleeps for a short time (used to yield to the UI / drive animations).

**Tags**
- ui

**Syntax**
- `AWAIT`
- `AWAIT <timeMs>`

**Arguments**
- `<timeMs>` (optional, int; default `0`): sleep duration in milliseconds after processing pending UI events. Must satisfy `0 <= timeMs <= 10000`.

**Semantics**
- Forces a repaint, sets an internal “sleep” state, processes UI events, and then:
  - if `timeMs > 0`, sleeps for `timeMs` milliseconds,
  - otherwise returns immediately after event processing.
- This is a redraw/UI-yield primitive, not a normal input wait and not a normal output producer.
- It does not assign `RESULT`/`RESULTS`.
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.

**Errors & validation**
- Runtime error if `timeMs < 0` or `timeMs > 10000`.

**Examples**
- `AWAIT`         ; yield to UI
- `AWAIT 16`      ; ~60 FPS pacing

**Progress state**
- complete
