**Summary**
- `PRINTDATAK` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Syntax**
- `PRINTDATAK [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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
- `PRINTDATAK CHOICE` ... `ENDDATA`

**Progress state**
- complete
