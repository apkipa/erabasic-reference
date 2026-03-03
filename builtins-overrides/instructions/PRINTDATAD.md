**Summary**
- `PRINTDATAD` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Syntax**
- `PRINTDATAD [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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
- `PRINTDATAD CHOICE` ... `ENDDATA`

**Progress state**
- complete
