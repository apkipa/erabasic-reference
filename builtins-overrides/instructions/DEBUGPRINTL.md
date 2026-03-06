**Summary**
- Like `DEBUGPRINT`, but also appends a newline to the debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINTL`
- `DEBUGPRINTL <raw text>`
- `DEBUGPRINTL;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw literal text, not an expression.

**Semantics**
- Same destination and isolation rules as `DEBUGPRINT`: it writes only to the separate debug-output buffer, not to the normal output model.
- After appending the raw literal text, appends one newline to the debug-output buffer.
- If debug mode is disabled, the instruction still executes but produces no visible effect.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DEBUGPRINTL init ok`

**Progress state**
- complete
