**Summary**
- Begins a `REPEAT ... REND` counted loop using the built-in variable `COUNT` as the loop counter.

**Tags**
- control-flow

**Syntax**
```text
REPEAT [<countExpr>]
    ...
REND
```

- Header line: `REPEAT [<countExpr>]`
- Terminator line: `REND`

**Arguments**
- `<countExpr>` (optional, int; default `0`; omission emits a warning): number of iterations.


**Semantics**
- `REPEAT` is implemented as a FOR-like loop over `COUNT:0`:
  - Initializes `COUNT:0` to `0`.
  - Uses `end = <countExpr>` and `step = 1`.
  - The loop continues while `COUNT:0 < end`.
- If `end <= 0`, the loop body is skipped.
- `COUNT:0` is incremented by `1` at `REND` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).
- Jump behavior note: control transfers between `REPEAT` and `REND` are done via their marker lines, and entering a marker line as a jump target begins execution at the following logical line:
  - Jumping to `REPEAT` re-enters at the first line of the body.
  - Jumping to `REND` exits to the first line after `REND`.

**Errors & validation**
- If the system variable `COUNT` is forbidden by the current variable-scope configuration, `REPEAT` raises an error when execution reaches the `REPEAT` line and its argument is parsed.
- If a constant count is `<= 0`, the engine emits a warning when the line’s argument is parsed.
- Nested `REPEAT` is warned about by the loader (not necessarily a hard error).

**Examples**
```erabasic
REPEAT 10
    PRINTV COUNT
REND
```

**Progress state**
- complete
