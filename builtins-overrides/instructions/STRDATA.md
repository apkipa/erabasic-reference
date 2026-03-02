**Summary**
- Like `PRINTDATA`, but instead of printing, it selects a `DATA`/`DATAFORM` choice and concatenates it into a destination string variable.

**Syntax**
- `STRDATA [<strVarTerm>]` ... `ENDDATA`

**Arguments**
- Optional `<strVarTerm>`: changeable string variable term to receive the result.
- If omitted, defaults to `RESULTS` (engine behavior).

**Defaults / optional arguments**
- Destination defaults to `RESULTS` when omitted.

**Semantics**
- Shares the same block structure as `PRINTDATA` (`DATA`, `DATAFORM`, `DATALIST`, `ENDDATA`).
- Selects one entry uniformly at random.
- Concatenates the selected lines with `\n` between them (for `DATALIST` multi-line entries).
- Stores the result into the destination variable and jumps to `ENDDATA`.

**Errors & validation**
- The destination must be a changeable string variable term.
- Same structural diagnostics as `PRINTDATA`.

**Examples**
```erabasic
STRDATA
  DATA Hello
  DATA World
ENDDATA
PRINTFORML RESULTS
```
