**Summary**
- Checks whether a named `DataTable` exists.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_EXIST(tableName)`

**Signatures / argument rules**
- `DT_EXIST(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- Returns `1` if the table exists.
- Returns `0` otherwise.

**Errors & validation**
- None.

**Examples**
- `IF DT_EXIST("db")`

**Progress state**
- complete
