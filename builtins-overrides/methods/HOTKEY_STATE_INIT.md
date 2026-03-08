**Summary**
- Allocates/reinitializes the host hotkey state array used by the optional hotkey subsystem.

**Tags**
- input
- host

**Syntax**
- `HOTKEY_STATE_INIT(size)`

**Signatures / argument rules**
- `HOTKEY_STATE_INIT(size)` → `long`

**Arguments**
- `size` (int): new state-array length.

**Semantics**
- Allocates a new hotkey state array of length `size`.
- Any previous hotkey state array contents are discarded.
- This prepares the array later used by `HOTKEY_STATE` and the optional hotkey subsystem.
- Returns `0`.

**Errors & validation**
- Runtime error if `size` is negative or otherwise invalid for array allocation.

**Examples**
- `HOTKEY_STATE_INIT(8)`

**Progress state**
- complete
