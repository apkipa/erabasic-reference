**Summary**
- `PRINTDATAL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAL [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAL [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

**Arguments**
- Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - (Honors `SETCOLOR` color.)
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
```erabasic
PRINTDATAL CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

**Progress state**
- complete
