**Summary**
- Like `WAIT`, but stops “message skip” from auto-advancing past the wait.

**Tags**
- io

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Semantics**
- Waits for Enter/click, and stops “message skip” from auto-advancing past the wait.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- None.

**Examples**
- `FORCEWAIT`

**Progress state**
- complete
