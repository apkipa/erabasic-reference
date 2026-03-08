**Summary**
- Timed wait: waits for a limited time (and optionally disallows user input), then continues.

**Tags**
- io

**Syntax**
- `TWAIT <timeMs>, <mode>`

**Arguments**
- `<timeMs>` (int): time limit in milliseconds.
- `<mode>` (int):
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Semantics**
- Observable visibility rule: by the time the instruction has put the console into its timed wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- See also: `input-flow.md` (shared wait-state lifecycle, timed completion model, and `MesSkip` auto-advance behavior).
- If `<mode> == 0`: enters the same Enter/click confirmation wait surface as `WAIT`, but with a time limit.
- If `<mode> != 0`: enters a no-input timed wait. Ordinary textbox/button submission does not satisfy it. Execution continues only when the time limit expires, or when skip/macro-driven continuation bypasses the wait under the shared non-value-wait rules.
- When the time limit elapses, execution continues automatically.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `TWAIT 3000, 0` (wait up to 3 seconds for Enter)
- `TWAIT 1000, 1` (wait 1 second with no input)

**Progress state**
- complete
