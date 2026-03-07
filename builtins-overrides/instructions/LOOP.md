**Summary**
- Ends a `DO ... LOOP` loop and provides the loop condition.

**Tags**
- control-flow

**Syntax**
- `LOOP [<int expr>]`

**Arguments**
- `<int expr>` (optional, int; default `0`; omission emits a warning): loop condition (`0` = false, non-zero = true).

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
