**Summary**
- Deletes the last *N logical output lines* from the console display/log.

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>`: integer expression (cast to a 32-bit signed integer before use; out-of-range values are implementation-defined).

**Defaults / optional arguments**
- None.

**Semantics**
- Evaluates `<n>` and calls the console’s internal `deleteLine(<n>)`.
- The deletion count is in **logical lines**, not raw display lines:
  - One logical line can occupy multiple display lines (e.g. word wrapping).
  - Deletion walks backward from the end of the display list and counts only entries marked as “logical line” boundaries; all associated display lines are removed.
- After deleting, the console is refreshed (`RefreshStrings(false)`).

**Errors & validation**
- No explicit validation in the instruction.
- Engine behavior is only well-defined for small non-negative `<n>`; negative or overflowed values can lead to implementation-specific results.

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

**Progress state**
- complete

