**Summary**
- Adds one or more new characters by copying an existing character’s data.

**Tags**
- characters

**Syntax**
- `ADDCOPYCHARA charaIndex`
- `ADDCOPYCHARA charaIndex1, charaIndex2, ...`

**Arguments**
- Each `charaIndex` (int): selects an existing character index to copy from.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaIndex` (evaluated and executed left-to-right), the engine:
  - Validates the source index is in range; otherwise errors.
  - Appends a new pseudo character.
  - Copies all character data from the source character into the newly appended last character.
- `CHARANUM` increases by 1 for each successfully created copy.
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- Runtime error if any `charaIndex` is out of range.

**Examples**
```erabasic
ADDCOPYCHARA 0
```

**Progress state**
- complete
