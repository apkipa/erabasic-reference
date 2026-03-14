**Summary**
- `PRINTDATADW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATADW [<intVarTerm>]
    ... data block body ...
ENDDATA
```
- `PRINTDATADW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATADW CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
