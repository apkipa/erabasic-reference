**Summary**
- Writes one entry in the host hotkey state array used by the optional hotkey subsystem.

**Tags**
- input
- host

**Syntax**
- `HOTKEY_STATE(index, value)`

**Signatures / argument rules**
- `HOTKEY_STATE(index, value)` → `long`

**Arguments**
- `index` (int): state-array index to update.
- `value` (int): new value to store.

**Semantics**
- Writes `state[index] = value` in the host hotkey state array.
- This affects only the optional host hotkey subsystem; by itself it does not enable hotkeys.
- Returns `0`.

**Errors & validation**
- Runtime error if the state array was not initialized first via `HOTKEY_STATE_INIT`.
- Runtime error if `index` is outside the allocated state-array bounds.

**Examples**
- `HOTKEY_STATE(2, 1)`

**Progress state**
- complete
