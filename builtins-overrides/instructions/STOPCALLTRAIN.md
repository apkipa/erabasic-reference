**Summary**
- Stops “continuous train command execution” mode (started by `CALLTRAIN`) and clears any remaining queued commands.

**Tags**
- system

**Syntax**
- `STOPCALLTRAIN`

**Arguments**
- None.

**Semantics**
- If continuous-train mode is active:
  - Clears the queued command list.
  - Calls `@CALLTRAINEND` if it exists.
- If not active, no-op.

**Errors & validation**
- (none)

**Examples**
- `STOPCALLTRAIN`

**Progress state**
- complete
