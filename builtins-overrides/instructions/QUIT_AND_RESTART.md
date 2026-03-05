**Summary**
- Requests the console to quit and restart the application.

**Tags**
- system

**Syntax**
- `QUIT_AND_RESTART`

**Arguments**
- None.

**Semantics**
- Sets the engine’s “reboot on quit” flag, then requests quit (same as `QUIT` for script control flow).
- Script execution stops immediately.
- The actual restart is performed by the UI host after the quit request is posted (typically on the next user interaction in the quit state).

**Errors & validation**
- (none)

**Examples**
- `QUIT_AND_RESTART`

**Progress state**
- complete
