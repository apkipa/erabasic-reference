**Summary**
- Returns the first chara index (role index) in the current character list whose character-data cell equals a target value.

**Tags**
- characters

**Syntax**
- `FINDCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`

**Signatures / argument rules**
- `FINDCHARA(charaVarTerm, value)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data variable term): selects a character-data variable (scalar or array).
  - If it is an array, its subscripts (written after the chara selector) select which per-chara cell is compared.
  - If it is an array, those subscript expressions are evaluated once to select the element(s) to compare.
- The chara selector part of `charaVarTerm` does not affect the search: the function always compares against the scanned chara index `i`.
  - The written chara selector is also not evaluated (no side effects from that expression).
- `value` (int|string; must match the selected cell type): scalar value to match.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `lastIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Reads the current `CHARANUM` and searches forward in the half-open range `[startIndex, lastIndex)`.
- For each chara index `i` in the range, compares the selected per-chara cell against `value` using direct equality:
  - string cell: `==` (ordinal string equality in .NET)
  - int cell: `==`
- Returns the first matching index `i`, or `-1` if:
  - no match is found, or
  - `startIndex >= lastIndex`.

**Errors & validation**
- Errors if `charaVarTerm` is not a character-data variable term, or if `value`’s type does not match the cell type.
- Runtime errors if the range is invalid:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `lastIndex < 0` or `lastIndex > CHARANUM`
- Note: `startIndex >= lastIndex` is not an error; it returns `-1`.

**Examples**
- `idx = FINDCHARA(NAME, "Alice")`
- `idx = FINDCHARA(CFLAG:3, 1, 10)`

**Progress state**
- complete
