**Summary**
- Deletes the last *N logical output lines* from the console display/log.

**Tags**
- io

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>`: integer expression.
  - The evaluated value is converted to a 32-bit signed integer by truncation (i.e. low 32 bits interpreted as signed).

**Semantics**
- Evaluates `<n>` and deletes the last `n` logical output lines from the console display/log.
- The deletion count is in **logical lines**, not raw display lines:
  - One logical line can occupy multiple display lines (e.g. word wrapping).
  - Deletion walks backward from the end of the display list and counts only entries marked as “logical line” boundaries; all associated display lines are removed.
- If `n <= 0`, nothing is deleted.
- After deleting, the display is refreshed.

**Errors & validation**
- No explicit validation in the instruction.
- No error is raised for negative or overflowed values (after the 32-bit conversion).

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

**Progress state**
- complete
