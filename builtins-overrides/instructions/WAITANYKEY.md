**Summary**
- Like `WAIT`, but accepts **any key** input (not only Enter) to continue.

**Tags**
- io

**Syntax**
- `WAITANYKEY`

**Arguments**
- None.

**Semantics**
- Observable visibility rule: by the time the instruction has put the console into its wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- Then enters an any-key confirmation wait. On this host, mouse left/right click can also satisfy that wait through the same UI continuation path.
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAITANYKEY`

**Progress state**
- complete
