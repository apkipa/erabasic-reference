**Summary**
- Writes a value, or `NULL`, into a selected cell of a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_SET(tableName, row, columnName)`
- `DT_CELL_SET(tableName, row, columnName, value)`
- `DT_CELL_SET(tableName, row, columnName, value, asId)`

**Signatures / argument rules**
- `DT_CELL_SET(tableName, row, columnName)` → `long`
- `DT_CELL_SET(tableName, row, columnName, value)` → `long`
- `DT_CELL_SET(tableName, row, columnName, value, asId)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `value` (optional, int|string): replacement value; omission writes `NULL`.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index. This slot is available only when `value` is present.

**Semantics**
- If the table does not exist, returns `-1`.
- If `columnName` resolves to `id` under case-insensitive comparison, returns `0` and refuses the write.
- If the selected row or column does not exist, returns `-3`.
- If `value` is omitted, writes `NULL` and returns `1`.
- If `value` is present but its type does not match the destination column type, returns `-2`.
- Integer writes to `int8` / `int16` / `int32` columns are clamped to the destination range.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- None beyond normal argument evaluation.

**Examples**
- `DT_CELL_SET("db", 0, "age", 18)`

**Progress state**
- complete
