**Summary**
- Appends raw literal text to the separate debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINT`
- `DEBUGPRINT <raw text>`
- `DEBUGPRINT;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw literal text, not an expression.

**Semantics**
- Appends the raw literal text to the host's **debug-output buffer**, not to the normal output model.
- Layer boundary:
  - this does not add normal display lines,
  - `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`, `LINECOUNT`, and `OUTPUTLOG` do not read it.
- If debug mode is disabled, the instruction still executes but produces no visible effect.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DEBUGPRINT trace=`

**Progress state**
- complete
