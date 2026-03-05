**Summary**
- Forces an immediate application restart (without waiting for the normal quit UI flow).

**Tags**
- system

**Syntax**
- `FORCE_QUIT_AND_RESTART`

**Arguments**
- None.

**Semantics**
- Sets the engine’s “reboot” flag and triggers the UI host’s restart routine immediately.
- Guard behavior (to prevent continuous restart without an intervening input wait):
  - If this instruction is executed again without passing through an input-wait/quit/error state, the engine shows a confirmation dialog.
  - If the user accepts, the engine cancels restart and raises a runtime error instead.

**Errors & validation**
- May raise a runtime error on the guard path (see above).

**Examples**
- `FORCE_QUIT_AND_RESTART`

**Progress state**
- complete
