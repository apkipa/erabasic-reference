**Summary**
- Starts a **multi-line** choice list inside a surrounding `PRINTDATA*` or `STRDATA` block.
- Each `DATA` / `DATAFORM` inside the list becomes a separate output line when this choice is selected.

**Tags**
- data-blocks

**Syntax**
- `DATALIST`
  - `DATA ...` / `DATAFORM ...` (one or more)
- `ENDLIST`

**Arguments**
- None.

**Semantics**
- At load time, the loader accumulates contained `DATA` / `DATAFORM` lines into a single list entry and attaches it to the surrounding `PRINTDATA*` / `STRDATA` block.

**Errors & validation**
- `DATALIST` must appear inside `PRINTDATA*` or `STRDATA`; otherwise it is a load-time error (the line is marked as error).
- Missing `ENDLIST` produces a load-time error at end of file/load.
- An empty list produces a non-fatal loader warning, but still creates an empty choice entry.

**Examples**
```erabasic
PRINTDATA
  DATALIST
    DATA Line 1
    DATA Line 2
  ENDLIST
ENDDATA
```

**Progress state**
- complete
