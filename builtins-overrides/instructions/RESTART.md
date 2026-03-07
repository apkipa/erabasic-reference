**Summary**
- Jumps back to the start of the currently executing function label without leaving the current call frame.

**Tags**
- flow

**Syntax**
- `RESTART`

**Arguments**
- None.

**Semantics**
- Restarts the current function label from its beginning.
- The current call frame is preserved: arguments, `LOCAL/LOCALS`, private variables, and other per-call state stay in the same call instance.
- In particular, `DYNAMIC` private variables are **not** reinitialized just because `RESTART` occurs.
- If the restarted function eventually returns, it returns to the original caller of the current function, not to the line after `RESTART`.
- Inside an event dispatch, `RESTART` restarts the current event handler label only; it does not restart the whole event-group sequence.

**Errors & validation**
- None.

**Examples**
- `RESTART`

**Progress state**
- complete
