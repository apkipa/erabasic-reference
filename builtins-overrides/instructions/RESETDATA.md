**Summary**
- Resets the current game/runtime variable state (excluding global variables).

**Tags**
- save-system

**Syntax**
- `RESETDATA`

**Arguments**
- None.

**Semantics**
- Resets the normal non-global resettable buckets to their default state:
  - local stores (`LOCAL/LOCALS`, `ARG/ARGS`),
  - static non-global user-defined variables,
  - non-global built-in variables.
- Disposes and clears the character list.
- Leaves built-in `GLOBAL/GLOBALS` and ERH `GLOBAL` user-defined variables untouched.
- Does **not** directly walk current live private `DYNAMIC` instances or private `REF` bindings; those disappear only when their owning call frames are later unwound or cleared.
- Removes Emuera-private save-related extension data (e.g. XML/maps/data-table extensions).
- Resets output style to defaults.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETDATA`

**Progress state**
- complete
