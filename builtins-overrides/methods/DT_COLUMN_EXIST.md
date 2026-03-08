**Summary**
- Checks whether a named `DataTable` contains a column and reports its type.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_EXIST(tableName, columnName)`

**Signatures / argument rules**
- `DT_COLUMN_EXIST(tableName, columnName)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (string): column name.

**Semantics**
- If the table does not exist, returns `-1`.
- If the column does not exist, returns `0`.
- Otherwise returns the type code `1=int8`, `2=int16`, `3=int32`, `4=int64`, or `5=string`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {DT_COLUMN_EXIST("db", "name")}`

**Progress state**
- complete
