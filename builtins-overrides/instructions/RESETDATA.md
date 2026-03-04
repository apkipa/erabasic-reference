**Summary**
- Resets the current game/runtime variable state (excluding global variables).

**Tags**
- save-system

**Syntax**
- `RESETDATA`

**Arguments**
- None.

**Semantics**
- Resets non-global variables to their default values (global variables are not reset).
- Disposes and clears the character list.
- Removes Emuera-private save-related extension data (e.g. XML/maps/data-table extensions).
- Resets output style to defaults.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETDATA`

**Progress state**
- complete
