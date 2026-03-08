**Summary**
- Removes a column from a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_REMOVE(tableName, columnName)`

**Signatures / argument rules**
- `DT_COLUMN_REMOVE(tableName, columnName)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (string): column name.

**Semantics**
- If the table does not exist, returns `-1`.
- If the column exists and its name is not `id` under case-insensitive comparison, removes it and returns `1`.
- If the column does not exist, or it resolves to the protected `id` column, returns `0`.

**Errors & validation**
- None.

**Examples**
- `DT_COLUMN_REMOVE("db", "age")`

**Progress state**
- complete
