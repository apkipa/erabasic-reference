**Summary**
- Like `WAIT`, but stops “message skip” from auto-advancing past the wait.

**Tags**
- io

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Semantics**
- Waits for Enter/click, and stops “message skip” from auto-advancing past the wait.
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `FORCEWAIT`

**Progress state**
- complete
