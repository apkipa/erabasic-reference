**Summary**
- Adds a “pseudo character” that is not loaded from CSV.

**Tags**
- characters

**Syntax**
- `ADDVOIDCHARA`

**Arguments**
- None.

**Semantics**
- Appends a new character record created from the engine’s pseudo-character template.
- The new character’s variables start from the language defaults (`0` for numeric cells, `""` for string reads).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- None specific to this instruction.

**Examples**
```erabasic
ADDVOIDCHARA
TARGET = CHARANUM - 1
```

**Progress state**
- complete
