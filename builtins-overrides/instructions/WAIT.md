**Summary**
- Waits for the user to press Enter (or click, depending on the UI), then continues.

**Syntax**
- `WAIT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Enters a UI wait state for an Enter-style key/click (`InputType.EnterKey`).
- Does not assign `RESULT`/`RESULTS`.
- If the script runner’s `skipPrint` mode is active (e.g. via `SKIPDISP`), `WAIT` is skipped as part of the print-family skip rule.

**Errors & validation**
- None.

**Examples**
- `WAIT`

**Progress state**
- complete
