**Summary**
- Clause header inside a `SELECTCASE ... ENDSELECT` block.

**Syntax**
- `CASE <caseExpr> (, <caseExpr> ... )`

**Arguments**
- Each `<caseExpr>` is one of:
  - Normal: `<expr>` (matches by equality against the selector).
  - Range: `<expr> TO <expr>` (inclusive range).
  - “IS form”: `IS <binaryOp> <expr>` (e.g. `IS >= 10`), using the engine’s binary-operator semantics.

**Defaults / optional arguments**
- None.

**Semantics**
- When reached **sequentially** (fall-through after another case body), `CASE` unconditionally jumps to the matching `ENDSELECT` marker, skipping the rest of the block.
- When entered as the selected clause, the engine jumps to the `CASE` header as a **marker** and begins executing at the next line (the clause body).

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) produces a load-time warning.
- An empty `CASE` condition list produces a load-time warning.
- A `TO` range requires both sides to have the same operand type.

**Examples**
- `CASE 5`
- `CASE 1 TO 10`
- `CASE IS >= 100`
