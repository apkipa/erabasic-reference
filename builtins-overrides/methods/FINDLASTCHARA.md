**Summary**
- Like `FINDCHARA`, but searches backward and returns the last matching chara index (role index) in the range.

**Tags**
- characters

**Syntax**
- `FINDLASTCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`

**Signatures / argument rules**
- `FINDLASTCHARA(charaVarTerm, value)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data variable term): selects a character-data variable (scalar or array).
  - If it is an array, its subscripts (written after the chara selector) select which per-chara cell is compared.
  - If it is an array, those subscript expressions are evaluated once to select the element(s) to compare.
- The chara selector part of `charaVarTerm` (written selector only): does not affect the search; the function always compares against the scanned chara index `i`.
  - The written chara selector is also not evaluated (no side effects from that expression).
- `value` (int|string; must match the selected cell type): scalar value to match.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `lastIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Reads the current `CHARANUM` and searches backward in the half-open range `[startIndex, lastIndex)`.
- The search order is: `lastIndex - 1`, `lastIndex - 2`, ..., down to `startIndex`.
- For each chara index `i` in the range, compares the selected per-chara cell against `value` using direct equality:
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
