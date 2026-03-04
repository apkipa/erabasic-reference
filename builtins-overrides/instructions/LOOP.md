**Summary**
- Ends a `DO ... LOOP` loop and provides the loop condition.

**Tags**
- control-flow

**Syntax**
- `LOOP <int expr>`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

- Omitted arguments / defaults:
  - If omitted, the condition defaults to `0` (false) and emits a load-time warning.

**Semantics**
- Evaluates the condition:
  - If true, jumps back to the matching `DO` marker (and continues at the first body line).
  - If false, falls through to the next line after `LOOP`.

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the line is marked as error).

**Examples**
- `LOOP I < 10`

**Progress state**
- complete
