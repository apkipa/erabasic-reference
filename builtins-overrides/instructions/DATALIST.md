**Summary**
- Starts a **multi-line** choice list inside a surrounding `PRINTDATA*` or `STRDATA` block.
- Each `DATA` / `DATAFORM` inside the list becomes a separate output line when this choice is selected.

**Syntax**
- `DATALIST`
  - `DATA ...` / `DATAFORM ...` (one or more)
- `ENDLIST`

**Arguments**
- None.

**Defaults / optional arguments**
- N/A.

**Semantics**
- At load time, the loader accumulates contained `DATA` / `DATAFORM` lines into a single list entry and attaches it to the surrounding `PRINTDATA*` / `STRDATA` block.

**Errors & validation**
- `DATALIST` outside `PRINTDATA*` / `STRDATA` is rejected by the loader.
- Missing `ENDLIST` produces loader diagnostics; an empty list produces a warning.

**Examples**
```erabasic
PRINTDATA
  DATALIST
    DATA Line 1
    DATA Line 2
  ENDLIST
ENDDATA
```
