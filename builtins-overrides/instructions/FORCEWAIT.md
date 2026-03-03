**Summary**
- Like `WAIT`, but stops “message skip” from auto-advancing past the wait.

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Enters an Enter-style UI wait (`InputType.EnterKey`) with `StopMesskip = true`.
  - Implementation detail: this prevents `MesSkip`-driven macro/skip logic from treating the wait as a no-op.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- None.

**Examples**
- `FORCEWAIT`

**Progress state**
- complete
