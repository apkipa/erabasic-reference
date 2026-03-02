**Summary**
- Begins a `REPEAT ... REND` counted loop using the built-in variable `COUNT` as the loop counter.

**Syntax**
- `REPEAT <countExpr>`
  - `...`
  - `REND`

**Arguments**
- `<countExpr>`: int expression giving the number of iterations.

**Defaults / optional arguments**
- If omitted, the count defaults to `0` (and emits a load-time warning).

**Semantics**
- `REPEAT` is implemented as a FOR-like loop over `COUNT:0`:
  - Initializes `COUNT:0` to `0`.
  - Uses `end = <countExpr>` and `step = 1`.
  - The loop continues while `COUNT:0 < end`.
- `COUNT:0` is incremented by `1` at `REND` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).
- Because the engine advances to `NextLine` before executing, jumps between `REPEAT` and `REND` are done via marker lines:
  - Jumping to `REPEAT` re-enters at the first line of the body.
  - Jumping to `REND` exits to the first line after `REND`.

**Errors & validation**
- If the system variable `COUNT` is forbidden by the current variable-scope configuration, `REPEAT` is rejected at load time.
- If a constant count is `<= 0`, the engine emits a warning.
- Nested `REPEAT` is warned about by the loader (not necessarily a hard error).

**Examples**
- `REPEAT 10`
- `  PRINTV COUNT`
- `REND`
