**Summary**
- Returns the column count of a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_LENGTH(tableName)`

**Signatures / argument rules**
- `DT_COLUMN_LENGTH(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise returns the current number of columns, including the auto-created `id` column.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {DT_COLUMN_LENGTH("db")}`

**Progress state**
- complete
