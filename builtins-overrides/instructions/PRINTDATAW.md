**Summary**
- `PRINTDATAW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAW [<intVarTerm>]
    ... data block body ...
ENDDATA
```
- `PRINTDATAW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATAW CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
