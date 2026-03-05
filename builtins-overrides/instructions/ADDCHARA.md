**Summary**
- Adds one or more characters to the current character list using character templates loaded from CSV.

**Tags**
- characters

**Syntax**
- `ADDCHARA charaNo`
- `ADDCHARA charaNo1, charaNo2, ...`

**Arguments**
- Each `charaNo`: int expression selecting a character template.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaNo` (evaluated left-to-right), the engine immediately appends one character to the current character list using the character template identified by that number.
- `CHARANUM` increases by 1 for each successfully added character.
- If a later argument fails (e.g. undefined template), earlier additions remain (no rollback).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- Runtime error if any `charaNo` does not resolve to a known character template.

**Examples**
```erabasic
ADDCHARA 3, 5, 6
PRINTFORML {CHARANUM}
```

**Progress state**
- complete
