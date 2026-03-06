**Summary**
- Clears the separate debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGCLEAR`

**Arguments**
- None.

**Semantics**
- Clears the host's debug-output buffer.
- This does not affect the normal output model, the pending print buffer, or the HTML-island layer.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DEBUGCLEAR`

**Progress state**
- complete
