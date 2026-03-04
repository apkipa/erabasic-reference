**Summary**
- Like `WAIT`, but accepts **any key** input (not only Enter) to continue.

**Tags**
- io

**Syntax**
- `WAITANYKEY`

**Arguments**
- None.

**Semantics**
- Enters a UI wait state for any-key input (`InputType.AnyKey`).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- None.

**Examples**
- `WAITANYKEY`

**Progress state**
- complete
