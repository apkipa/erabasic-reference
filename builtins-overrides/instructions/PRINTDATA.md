**Summary**
- Begins a **PRINTDATA block** that contains `DATA` / `DATAFORM` (and optional `DATALIST` groups).
- At runtime, the engine picks one choice uniformly at random, prints it, then jumps to `ENDDATA`.

**Syntax**
- `PRINTDATA [<intVarTerm>]`
- Block form:
  - `PRINTDATA [<intVarTerm>]`
    - `DATA <raw text>` / `DATAFORM <FORM string>` (one or more choices)
    - optionally, `DATALIST` ... `ENDLIST` groups to make a multi-line choice
  - `ENDDATA`

**Arguments**
- Optional `<intVarTerm>`: a changeable int variable term that receives the 0-based chosen index.

**Defaults / optional arguments**
- If `<intVarTerm>` is omitted, the chosen index is not stored anywhere.

**Semantics**
- Load-time structure rules (enforced by the loader):
  - `PRINTDATA*` must be closed by a matching `ENDDATA`.
  - `DATA` / `DATAFORM` must appear inside `PRINTDATA*`, `STRDATA`, or inside a `DATALIST` that is itself inside one of those blocks.
  - Nested `PRINTDATA*` blocks are rejected (warning/error).
  - `STRDATA` cannot be nested inside `PRINTDATA*` and vice versa (warning/error).
- Runtime behavior:
  - If there are no `DATA` choices, nothing is printed and the engine jumps to `ENDDATA`.
  - Otherwise:
    - Choose `choice = RAND(0..count-1)` using the engine RNG.
    - If `<intVarTerm>` is present, assign it the chosen index.
    - Print the selected `DATA` entry:
      - A single `DATA`/`DATAFORM` line prints as one line.
      - A `DATALIST` entry prints each contained `DATA`/`DATAFORM` line separated by newlines.
    - If the keyword has `...L`/`...W` behavior, append a newline (and optionally wait for a key).
    - Jump to the `ENDDATA` line, skipping over the block body.

**Errors & validation**
- Errors/warnings for missing `ENDDATA`, `DATA` outside a block, `ENDLIST` without `DATALIST`, etc., are produced by the loader.
- The optional `<intVarTerm>` must be a changeable int variable term.

**Examples**
```erabasic
PRINTDATA CHOICE
  DATA First option
  DATA Second option
ENDDATA
```

```erabasic
PRINTDATA
  DATALIST
    DATA Line 1
    DATAFORM Line 2: %TOSTR(RAND:100)%
  ENDLIST
ENDDATA
```
