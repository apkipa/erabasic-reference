**Summary**
- `PRINTDATAKW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAKW [<intVarTerm>]
    ... data block body ...
ENDDATA
```
- `PRINTDATAKW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATAKW CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
