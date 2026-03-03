**Summary**
- `PRINTDATAL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Syntax**
- `PRINTDATAL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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
- `PRINTDATAL CHOICE` ... `ENDDATA`

**Progress state**
- complete
