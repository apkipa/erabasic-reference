**Summary**
- Ends a `REPEAT ... REND` loop.

**Tags**
- control-flow

**Syntax**
- `REND`

**Arguments**
- None.

**Semantics**
- Increments the loop counter and decides whether to continue:
  - If more iterations remain, jumps back to the matching `REPEAT` marker (and thus continues at the first body line).
  - Otherwise falls through to the next line after `REND`.
- Engine quirk: if the loop counter state is missing (e.g. due to invalid jumps into/out of the loop), `REND` exits the loop instead of throwing.

**Errors & validation**
- `REND` without a matching open `REPEAT` is a load-time error (the line is marked as error).

**Examples**
```erabasic
REPEAT 10
    PRINTV COUNT
REND
```

**Progress state**
- complete
