**Summary**
- Checks whether a selected cell is `NULL` in a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_ISNULL(tableName, row, columnName [, asId])`

**Signatures / argument rules**
- `DT_CELL_ISNULL(tableName, row, columnName)` → `long`
- `DT_CELL_ISNULL(tableName, row, columnName, asId)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index.

**Semantics**
- If the table does not exist, returns `-1`.
- If the selected row or column does not exist, returns `-2`.
- Otherwise returns `1` when the selected cell contains `NULL`, or `0` when it contains a value.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- None.

**Examples**
- `IF DT_CELL_ISNULL("db", id, "age", 1)`

**Progress state**
- complete
