**Summary**
- Resets the current game/runtime variable state (excluding global variables).

**Syntax**
- `RESETDATA`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Calls `VEvaluator.ResetData()`, which (high-level):
  - Clears local/default variable state.
  - Disposes and clears the character list.
  - Removes certain Emuera-private save-related data structures (implementation detail; e.g. XML/maps/DT savedata extensions).
  - Does **not** reset global variables.
- Resets console style (`Console.ResetStyle()`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETDATA`

**Progress state**
- complete

