**Summary**
- Ends a `DO ... LOOP` loop and provides the loop condition.

**Syntax**
- `LOOP <int expr>`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

**Defaults / optional arguments**
- If omitted, the condition defaults to `0` (false) and emits a load-time warning.

**Semantics**
- Evaluates the condition:
  - If true, jumps back to the matching `DO` marker (and continues at the first body line).
  - If false, falls through to the next line after `LOOP`.

**Errors & validation**
- `LOOP` without a matching open `DO` produces a load-time warning.

**Examples**
- `LOOP I < 10`
