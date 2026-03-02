**Summary**
- Returns the first character index in the current character list whose character-variable cell equals a target value.

**Signatures / argument rules**
- `FINDCHARA(charaVarTerm, value)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm`: character-data variable term (may be array; element indices taken from subscripts after the character selector).
- `value`: same scalar type as the variable (string or int).
- `startIndex` (optional, default `0`): inclusive start.
- `lastIndex` (optional, default `CHARANUM`): exclusive end.

**Semantics**
- Searches forward in `[startIndex, lastIndex)`; returns matching index or `-1` if not found or if `startIndex >= lastIndex`.
- Equality check is direct (`==`) on the per-character cell value.

**Errors & validation**
- Errors if `startIndex`/`lastIndex` are out of range.
- Errors if `charaVarTerm` is not a character-data variable term.

**Examples**
- `idx = FINDCHARA(NAME, "Alice")`
- `idx = FINDCHARA(CFLAG:3, 1, 10)`
