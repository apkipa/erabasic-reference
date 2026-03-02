**Summary**
- Returns a substring where `start`/`length` are measured in the engine’s current language-encoding byte count (not Unicode code units).

**Signatures / argument rules**
- `SUBSTRING(str)` → `string`
- `SUBSTRING(str, start)` → `string`
- `SUBSTRING(str, start, length)` → `string`

**Arguments**
- `str`: string.
- `start` (optional): int (byte offset, 0-based).
- `length` (optional): int (byte length; `<0` means “to end”).

**Semantics**
- Uses the engine’s encoding-aware substring routine.
- If `start >= totalByte` or `length == 0`: returns `""`.
- If `length < 0` or `length > totalByte`: treated as `totalByte`.
- Does not split characters: advances by character while tracking encoded byte counts.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.

**Examples**
- `SUBSTRING("ABCDE", 1, 2)` → `"BC"` (ASCII)
