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
- The UI host performs the actual restart after the quit request is posted; scripts have no further control over that timing.

**Errors & validation**
- (none)

**Examples**
- `QUIT_AND_RESTART`

**Progress state**
- complete
