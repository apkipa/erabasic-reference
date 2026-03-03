**Summary**
- Default clause header inside a `SELECTCASE ... ENDSELECT` block.

**Syntax**
- `CASEELSE`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Chosen only if no earlier `CASE` matches.
- When reached **sequentially** (fall-through after another case body), `CASEELSE` unconditionally jumps to the matching `ENDSELECT` marker.
- When selected, the engine jumps to the `CASEELSE` header as a **marker** and begins executing at the next line (the clause body).

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) is a load-time error (the line is marked as error).
- `CASE` after `CASEELSE` produces a load-time warning.

**Examples**
- `CASEELSE`

**Progress state**
- complete
