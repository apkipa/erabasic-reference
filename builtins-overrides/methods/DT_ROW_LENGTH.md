**Summary**
- Returns the row count of a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_LENGTH(tableName)`

**Signatures / argument rules**
- `DT_ROW_LENGTH(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise returns the current row count.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {DT_ROW_LENGTH("db")}`

**Progress state**
- complete
