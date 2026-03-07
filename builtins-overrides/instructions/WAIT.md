**Summary**
- Waits for a confirmation event, then continues.

**Tags**
- io

**Syntax**
- `WAIT`

**Arguments**
- None.

**Semantics**
- Observable visibility rule: by the time the instruction has put the console into its wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- Then enters an Enter-style confirmation wait. On this host, that wait can be satisfied by Enter and by the same left/right-click UI path used for ordinary `WAIT` continuation.
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAIT`

**Progress state**
- complete
