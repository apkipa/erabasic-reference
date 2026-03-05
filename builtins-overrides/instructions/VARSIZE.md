**Summary**
- Writes the size of an array variable into `RESULT` / `RESULT:1` / `RESULT:2`.

**Tags**
- variables

**Syntax**
- `VARSIZE <arrayVarName>`

**Arguments**
- `<arrayVarName>`: an identifier token naming an array variable (not an expression).
  - Must be a 1D/2D/3D array variable (character-data arrays are allowed).
  - `RAND` is rejected (even though it is 1D).
  - Compatibility parsing: any extra characters after the identifier are ignored (with a warning). For example, `VARSIZE ABL:TARGET:0` is treated like `VARSIZE ABL`.
    - The ignored tail is not parsed as expressions and is not evaluated (so it has no side effects).

**Semantics**
- Resolves `<arrayVarName>` to a variable token.
- Writes array lengths into `RESULT_ARRAY`:
  - 1D array: `RESULT = length0`
  - 2D array: `RESULT = length0`, `RESULT:1 = length1`
  - 3D array: `RESULT = length0`, `RESULT:1 = length1`, `RESULT:2 = length2`
- Does not clear other `RESULT:*` slots.

**Errors & validation**
- Errors if `<arrayVarName>` is missing, is not a variable identifier, is not an array variable, or is `RAND`.

**Examples**
- `VARSIZE ABL` (writes the `ABL` dimensions to `RESULT*`)
- `VARSIZE ITEM` (writes the `ITEM` length to `RESULT`)

**Progress state**
- complete
