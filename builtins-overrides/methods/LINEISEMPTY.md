**Summary**
- Returns whether the current in-progress output line is still empty.

**Tags**
- io

**Syntax**
- `LINEISEMPTY()`

**Signatures / argument rules**
- `LINEISEMPTY()` → `long`

**Arguments**
- None.

**Semantics**
- Returns `1` if the current printable line buffer has no content yet.
- Returns `0` once the current line has any visible/button content pending on it.
- Equivalent observable test: at that point in execution, would a bare `PRINTL` emit only an empty line?
- Only the current in-progress line matters; already flushed earlier lines do not affect the result.

**Errors & validation**
- None.

**Examples**
- `IF LINEISEMPTY() != 0`

**Progress state**
- complete
