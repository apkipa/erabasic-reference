**Summary**
- Ends a `SELECTCASE ... ENDSELECT` block.

**Syntax**
- `ENDSELECT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader uses it to close `SELECTCASE` nesting and to set jump targets for `SELECTCASE`/`CASE`/`CASEELSE`.

**Errors & validation**
- `ENDSELECT` without a matching open `SELECTCASE` is a load-time error (the line is marked as error).

**Examples**
- `ENDSELECT`

**Progress state**
- complete
