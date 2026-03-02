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
- `ENDDATA` without an open `PRINTDATA*` / `STRDATA` produces loader diagnostics.
- Closing a block while a `DATALIST` is still open produces a loader diagnostic.

**Examples**
- (See `PRINTDATA`.)
