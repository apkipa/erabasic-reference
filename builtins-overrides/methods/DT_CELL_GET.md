**Summary**
- Reads a cell as an integer from a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_GET(tableName, row, columnName [, asId])`

**Signatures / argument rules**
- `DT_CELL_GET(tableName, row, columnName)` → `long`
- `DT_CELL_GET(tableName, row, columnName, asId)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index.

**Semantics**
- If the table does not exist, returns `0`.
- If the selected row or column does not exist, returns `0`.
- If the selected cell is `NULL`, returns `0`.
- Otherwise converts the stored value with `Convert.ToInt64(...)` and returns the result.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- Runtime error if the stored value cannot be converted to `long`. For example, a non-numeric string cell read through `DT_CELL_GET` throws instead of returning `0`.

**Examples**
- `PRINTFORML {DT_CELL_GET("db", 0, "age")}`

**Progress state**
- complete
