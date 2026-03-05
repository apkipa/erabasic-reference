**Summary**
- Swaps two entries in the engine’s current character list.

**Tags**
- characters

**Syntax**
- `SWAPCHARA x, y`

**Arguments**
- `x` (int): character index.
- `y` (int): character index.

**Semantics**
- If `x == y`, no-op.
- Otherwise, swaps the character objects at indices `x` and `y` in the current character list.
- Does not adjust `TARGET` / `ASSI` / `MASTER`:
  - they remain numeric indices, so after the swap they may refer to different character objects than before.
- Does not print output.

**Errors & validation**
- Runtime error if `x` or `y` is out of range (`x < 0`, `y < 0`, or `>= CHARANUM`).

**Examples**
- `SWAPCHARA 1, 2`

**Progress state**
- complete

