**Summary**
- Like `PRINTDATA`, but instead of printing, it selects a `DATA`/`DATAFORM` choice and concatenates it into a destination string variable.

**Tags**
- data-blocks

**Syntax**
```text
STRDATA [<strVarTerm>]
    DATA <raw text> | DATAFORM <formString>
    ...
    [DATALIST
        DATA <raw text> | DATAFORM <formString>
        ...
    ENDLIST]
ENDDATA
```

- Header line: `STRDATA [<strVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

**Arguments**
- `<strVarTerm>` (optional, changeable string variable term; default `RESULTS`): receives the result.


**Semantics**
- Shares the same block structure as `PRINTDATA` (`DATA`, `DATAFORM`, `DATALIST`, `ENDDATA`).
- Selects one entry uniformly at random.
- Concatenates the selected lines with `\n` between them (for `DATALIST` multi-line entries).
- Stores the result into the destination variable and jumps to `ENDDATA`.
- If the block contains no `DATA`/`DATAFORM` choices at all, it simply jumps to `ENDDATA` and does **not** assign anything to the destination variable (it remains unchanged).

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

**Progress state**
- complete
