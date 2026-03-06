**Summary**
- Waits for the user to press Enter (or click, depending on the UI), then continues.

**Tags**
- io

**Syntax**
- `WAIT`

**Arguments**
- None.

**Semantics**
- Enters a UI wait state for an Enter-style key/click.
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAIT`

**Progress state**
- complete
