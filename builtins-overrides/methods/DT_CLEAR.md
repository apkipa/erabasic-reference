**Summary**
- Removes all rows from a named `DataTable` without changing its columns.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CLEAR(tableName)`

**Signatures / argument rules**
- `DT_CLEAR(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise clears all rows, keeps the schema intact, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `DT_CLEAR("db")`

**Progress state**
- complete
