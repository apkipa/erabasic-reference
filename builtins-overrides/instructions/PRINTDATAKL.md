**Summary**
- `PRINTDATAKL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAKL [<intVarTerm>]
    ... data block body ...
ENDDATA
```
- `PRINTDATAKL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATAKL CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
