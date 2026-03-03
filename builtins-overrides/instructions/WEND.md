**Summary**
- Ends a `WHILE ... WEND` loop.

**Syntax**
- `WEND`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Re-evaluates the matching `WHILE` condition:
  - If true, jumps back to the `WHILE` marker (and continues at the first body line).
  - If false, falls through to the next line after `WEND`.

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the line is marked as error).

**Examples**
- `WEND`

**Progress state**
- complete
