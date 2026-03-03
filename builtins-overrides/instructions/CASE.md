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
- Matching rules (engine details):
  - Normal: `selector == expr` (strings use .NET `==` on `string`).
  - Range:
    - int: `left <= selector && selector <= right`
    - string: uses `string.Compare(left, selector, SCExpression)` and `string.Compare(selector, right, SCExpression)` (where `SCExpression` is the engine’s configured string-comparison mode for expressions).
  - `IS <op> <expr>`: evaluates `(selector <op> expr)` using the engine’s binary operator reducer.

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) is a load-time error (the line is marked as error).
- An empty `CASE` condition list is a load-time error (argument parsing fails and the line is marked as error).
- A `TO` range requires both sides to have the same operand type (otherwise: load-time error).

**Examples**
- `CASE 5`
- `CASE 1 TO 10`
- `CASE IS >= 100`

**Progress state**
- complete
