**Summary**
- `PRINTDATAK` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAK [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAK [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATAK CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
