**Summary**
- Returns the length of an array variable’s dimension.

**Tags**
- variables

**Syntax**
- `VARSIZE(varName [, dim])`

**Signatures / argument rules**
- `VARSIZE(varName)` → `int`
- `VARSIZE(varName, dim)` → `int`

**Arguments**
- `varName` (string): variable name to resolve.
  - This is a variable **name**, not a variable term. Do not include `:` indices (for example, `"CFLAG:TARGET:0"` does not resolve as a variable name).
- `dim` (optional, int; default `0`): dimension selector.
  - Default behavior: `0` selects the first dimension (0-based).
  - If `VarsizeDimConfig` is enabled and `dim > 0`, the engine subtracts `1` before selecting the dimension (i.e. `1` selects the first dimension).

**Semantics**
- Resolves `varName` to a variable token using the normal variable-name lookup rules.
- Returns `GetLength(dim)` of that variable token.
  - For a 1D array, valid `dim` is `0`.
  - For a 2D array, valid `dim` is `0` or `1`.
  - For a 3D array, valid `dim` is `0`, `1`, or `2`.
- Reference variables (`REF`) are supported as long as they currently refer to an array; otherwise it errors.

**Errors & validation**
- Runtime error if `varName` does not resolve to a variable.
- Runtime error if the resolved variable is not an array variable.
- Runtime error if `dim` is out of range for that variable’s dimension count (including negative values).
- Runtime error if the resolved variable is a `REF` variable that is currently unbound.

**Examples**
- `n = VARSIZE("ITEM")` (length of `ITEM`)
- `w = VARSIZE("CFLAG", 1)` (first dimension when `VarsizeDimConfig` is enabled)

**Progress state**
- complete
