**Summary**
- Updates persistent system-flow string-input mode and its stored default string.

**Tags**
- input
- system-flow

**Syntax**
- `FLOWINPUTS(enableStringMode [, defaultString])`

**Signatures / argument rules**
- `FLOWINPUTS(enableStringMode)` → `long`
- `FLOWINPUTS(enableStringMode, defaultString)` → `long`

**Arguments**
- `enableStringMode` (int): non-zero switches future system-flow waits to string-input mode; `0` switches them back to integer-input mode.
- `defaultString` (optional, string): stored default string for later system-flow waits.

**Semantics**
- This function does not perform an input wait by itself.
- It mutates persistent process-level state used later by system-flow waits.
- Field update rules:
  - `enableStringMode` is always overwritten,
  - `defaultString` is overwritten only when supplied,
  - omitted `defaultString` leaves the previous stored default string unchanged.
- When string mode is enabled, future system-flow waits request string input instead of integer input.
- The stored default string is injected into the actual wait request only when `FLOWINPUT`'s mouse/default mode is also enabled.
- These flags affect only system-flow waits built on the engine's dedicated system-input path, not ordinary script `INPUT*` statements.
- Returns `0`.

**Errors & validation**
- None beyond normal argument evaluation.

**Examples**
- `FLOWINPUTS(1, "")`

**Progress state**
- complete
