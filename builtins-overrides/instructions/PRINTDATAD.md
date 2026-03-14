**Summary**
- `PRINTDATAD` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAD [<intVarTerm>]
    ... data block body ...
ENDDATA
```
- `PRINTDATAD [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - (No automatic newline suffix.)
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATAD CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
