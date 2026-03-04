**Summary**
- Skips to the next iteration of the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Tags**
- control-flow

**Syntax**
- `CONTINUE`

**Arguments**
- None.

**Semantics**
- The loader links `CONTINUE` to the nearest enclosing loop start marker.
- `REPEAT`/`FOR`: increments the loop counter by `step`, then either:
  - jumps back to the loop start marker (continue), or
  - jumps to the end marker (exit) if no iterations remain.
- `WHILE`: re-evaluates the condition and either continues or exits.
- `DO`: evaluates the matching `LOOP` condition and either continues or exits.

**Errors & validation**
- `CONTINUE` outside any loop is a load-time error (the line is marked as error).

**Examples**
- `CONTINUE`

**Progress state**
- complete
