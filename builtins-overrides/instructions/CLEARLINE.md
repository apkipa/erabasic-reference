**Summary**
- Deletes the last *N logical output lines* from the current visible normal output area.

**Tags**
- io

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>` (int): number of logical output lines to delete.
  - The evaluated value is converted to a 32-bit signed integer by truncation (low 32 bits interpreted as signed).

**Semantics**
- Evaluates `<n>` and deletes the last `n` logical lines from the current visible normal output area.
- The deletion count is in **logical lines**, not visible display rows:
  - one logical line can occupy multiple visible display rows,
  - deleting one logical line removes all of its visible rows.
- If the current trailing visible line is temporary and it falls within the deleted suffix, it is deleted like any other currently visible logical line.
- If `n <= 0`, nothing is deleted.
- Layer boundary:
  - this affects only the current visible normal output area,
  - it does not clear or flush the pending print buffer,
  - it does not affect the separate `HTML_PRINT_ISLAND` layer.
- After deleting, the display is refreshed.

**Errors & validation**
- No explicit validation in the instruction.
- No error is raised for negative or overflowed values after the 32-bit conversion.

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

**Progress state**
- complete
