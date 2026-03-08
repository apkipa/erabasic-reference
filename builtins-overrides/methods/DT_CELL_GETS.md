**Summary**
- Reads a cell as a string from a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_GETS(tableName, row, columnName [, asId])`

**Signatures / argument rules**
- `DT_CELL_GETS(tableName, row, columnName)` → `string`
- `DT_CELL_GETS(tableName, row, columnName, asId)` → `string`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index.

**Semantics**
- If the table does not exist, returns `""`.
- If the selected row or column does not exist, returns `""`.
- If the selected cell is `NULL`, returns `""`.
- Otherwise returns `value.ToString()`.
- Numeric cells therefore come back as their decimal string form.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- None.

**Examples**
- `PRINTFORM %DT_CELL_GETS("db", 0, "name")%`

**Progress state**
- complete
