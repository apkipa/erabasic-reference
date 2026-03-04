**Summary**
- Adds one or more “SP characters” using the SP-character template path.

**Tags**
- characters

**Syntax**
- `ADDSPCHARA charaNo`
- `ADDSPCHARA charaNo1, charaNo2, ...`

**Arguments**
- Each `charaNo`: int expression selecting a character template.

**Semantics**
- Requires `Config.CompatiSPChara` to be enabled; otherwise this instruction errors before evaluating any arguments.
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses (argument-builder behavior for `INT_ANY`).
- For each `charaNo` (evaluated left-to-right), immediately appends one character using the SP template lookup path.
- `CHARANUM` increases by 1 for each successfully added character.
- If a later argument fails (e.g. undefined template), earlier additions remain (no rollback).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- Runtime error if `CompatiSPChara` is disabled.
- Runtime error if any `charaNo` does not resolve to a known character template.

**Examples**
```erabasic
ADDSPCHARA 10
```

**Progress state**
- complete
