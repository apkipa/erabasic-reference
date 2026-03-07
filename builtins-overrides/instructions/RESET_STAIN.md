**Summary**
- Resets one character’s `STAIN` array to the engine’s configured default stain table.

**Tags**
- characters

**Syntax**
- `RESET_STAIN <charaID>`

**Arguments**
- `<charaID>` (int): selects an existing registered character.

**Semantics**
- Replaces the target character’s entire `STAIN` array with the configured default stain values.
- The default table is the same one used for newly initialized stain state (including `_Replace.csv`-driven defaults when enabled; see `config-items.md`).
- If the target `STAIN` array is longer than the configured default table, the remaining tail elements are set to `0`.
- If the target `STAIN` array is shorter than the configured default table, only the leading portion that fits is copied.

**Errors & validation**
- Runtime error if `<charaID>` is outside the current registered-character range.

**Examples**
- `RESET_STAIN TARGET`

**Progress state**
- complete
