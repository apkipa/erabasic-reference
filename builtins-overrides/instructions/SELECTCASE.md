**Summary**
- Begins a `SELECTCASE ... ENDSELECT` multi-branch block that compares a single selector expression against one or more `CASE` conditions.

**Tags**
- control-flow

**Syntax**
```text
SELECTCASE <expr>
    CASE <caseExpr> [, <caseExpr> ...]
        ...
    ...
    [CASEELSE
        ...]
ENDSELECT
```

- Header line: `SELECTCASE <expr>`
- Clause header lines inside the block are `CASE <caseExpr> [, <caseExpr> ...]`; an optional final `CASEELSE` may appear.
- Terminator line: `ENDSELECT`

**Arguments**
- `<expr>` (int|string): selector expression.

**Semantics**
- The loader gathers all `CASE` / `CASEELSE` headers into an ordered list and links them to the matching `ENDSELECT`.
- At runtime:
  - Evaluates the selector once to either `long` or `string`.
  - Scans each `CASE` in order; the first `CASE` that matches becomes the chosen clause.
  - If no `CASE` matches and a `CASEELSE` exists, chooses `CASEELSE`.
  - Otherwise jumps to the `ENDSELECT` marker (skipping the whole block).
- When a clause is chosen, the engine jumps to that `CASE`/`CASEELSE` header as a **marker** and begins executing at the next line (the clause body).

**Errors & validation**
- Missing selector expression is a load-time error (the `SELECTCASE` line is marked as error).
- `CASE` expressions whose type does not match the selector type are load-time errors (the `CASE` line is marked as error and is skipped by the runtime selector scan).
- Mis-nesting / unexpected `CASE` / unexpected `ENDSELECT` are load-time errors (the line is marked as error).

**Examples**
```erabasic
SELECTCASE A
CASE 0
    PRINTL "zero"
CASE 1 TO 9
    PRINTL "small"
CASEELSE
    PRINTL "other"
ENDSELECT
```

**Progress state**
- complete
