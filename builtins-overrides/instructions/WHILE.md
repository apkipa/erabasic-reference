**Summary**
- Begins a `WHILE ... WEND` loop.

**Syntax**
- `WHILE <int expr>`
  - `...`
  - `WEND`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

**Defaults / optional arguments**
- If omitted, the condition defaults to `0` (false) and emits a load-time warning.

**Semantics**
- At `WHILE`, evaluates the condition:
  - If true, enters the body (next line).
  - If false, jumps to the matching `WEND` marker (exiting the loop).
- At `WEND`, the engine re-evaluates the `WHILE` condition and loops again if it is still true.

**Errors & validation**
- `WEND` without a matching open `WHILE` produces a load-time warning.

**Examples**
- `WHILE I < 10`
- `  I += 1`
- `WEND`
