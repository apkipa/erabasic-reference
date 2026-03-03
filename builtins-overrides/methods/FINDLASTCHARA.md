**Summary**
- Like `FINDCHARA`, but searches backward and returns the last matching character index in the range.

**Syntax**
- `FINDLASTCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `FINDLASTCHARA(NAME, "A", , 10)`).

**Signatures / argument rules**
- `FINDLASTCHARA(charaVarTerm, value)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm`: character-data variable term.
  - Must evaluate to a variable term whose identifier is marked as “character data”.
  - If the variable is a 1D/2D array, the array subscripts on `charaVarTerm` select which per-character cell is compared.
- `value`: scalar value to match; must be the same scalar type as the selected cell (string vs int).
- `startIndex` (optional): int expression; inclusive start character index.
- `lastIndex` (optional): int expression; exclusive end character index.

**Defaults / optional arguments**
- If `startIndex` is omitted (or omitted as an empty slot): defaults to `0`.
- If `lastIndex` is omitted (or omitted as an empty slot): defaults to `CHARANUM` (the current total number of characters).

**Semantics**
- Reads the current `CHARANUM` and searches backward in the half-open range `[startIndex, lastIndex)`.
- The search order is: `lastIndex - 1`, `lastIndex - 2`, ..., down to `startIndex`.
- For each character index `i` in the range, compares `charaVarTerm(i)` against `value` using direct equality:
  - string cell: `==` (ordinal string equality in .NET)
  - int cell: `==`
- Returns the first match encountered in that reverse scan (i.e. the “last” match in the range), or `-1` if:
  - no match is found, or
  - `startIndex >= lastIndex`.

**Errors & validation**
- Errors if `charaVarTerm` is not a character-data variable term, or if `value`’s type does not match the cell type.
- Runtime errors if the range is invalid:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `lastIndex < 0` or `lastIndex > CHARANUM`
- Note: `startIndex >= lastIndex` is not an error; it returns `-1`.

**Examples**
- `idx = FINDLASTCHARA(NAME, "Alice")`
- `idx = FINDLASTCHARA(CFLAG:3, 1, 10)`

**Progress state**
- complete
