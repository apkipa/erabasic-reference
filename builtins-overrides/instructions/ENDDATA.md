**Summary**
- Closes a `PRINTDATA*` or `STRDATA` block.

**Syntax**
- `ENDDATA`

**Arguments**
- None.

**Defaults / optional arguments**
- N/A.

**Semantics**
- Load-time only structural marker. At runtime it does nothing.
- The loader wires `PRINTDATA*` / `STRDATA` to jump here after printing/selection.

**Errors & validation**
- `ENDDATA` without an open `PRINTDATA*` / `STRDATA` is a load-time error (the line is marked as error).
- Closing a block while a `DATALIST` is still open is a load-time error.

**Examples**
- (See `PRINTDATA`.)

**Progress state**
- complete
