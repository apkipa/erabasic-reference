**Summary**
- Ends a `FOR ... NEXT` loop.

**Tags**
- control-flow

**Syntax**
- `NEXT`

**Arguments**
- None.

**Semantics**
- Like `REND`, but paired with `FOR`.
- Increments the loop counter by `step`, then:
  - If more iterations remain, jumps back to the matching `FOR` marker (and continues at the first body line).
  - Otherwise falls through to the next line after `NEXT`.

**Errors & validation**
- `NEXT` without a matching open `FOR` is a load-time error (the line is marked as error).

**Examples**
- `NEXT`

**Progress state**
- complete
