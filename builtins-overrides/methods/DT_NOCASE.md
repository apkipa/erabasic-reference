**Summary**
- Toggles case-sensitive string comparison for a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_NOCASE(tableName, ignoreCase)`

**Signatures / argument rules**
- `DT_NOCASE(tableName, ignoreCase)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `ignoreCase` (int): non-zero makes the table case-insensitive; `0` restores case-sensitive comparison.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise sets `CaseSensitive` to `false` when `ignoreCase != 0`, or to `true` when `ignoreCase == 0`, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `DT_NOCASE("db", 1)`

**Progress state**
- complete
