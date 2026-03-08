**Summary**
- Adds a row to a named `DataTable` and returns its generated `id` value.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_ADD(tableName [, columnName, columnValue] ...)`
- `DT_ROW_ADD(tableName, columnNames, columnValues, count)`

**Signatures / argument rules**
- `DT_ROW_ADD(tableName)` → `long`
- `DT_ROW_ADD(tableName, columnName, columnValue [, columnName, columnValue] ...)` → `long`
- `DT_ROW_ADD(tableName, columnNames, columnValues, count)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (optional, string): column name in the variadic pair form.
- `columnValue` (optional, int|string): value in the variadic pair form; its type must match the destination column type.
- `columnNames` (string[]): column names in the array form.
- `columnValues` (int[]|string[]): homogeneous value array in the array form; mixed string/integer array input is not supported.
- `count` (int): requested number of array-form assignments.

**Semantics**
- If the table does not exist, returns `-1`.
- Creates a new row, auto-generates its `id`, then applies assignments.
- Calling `DT_ROW_ADD(tableName)` with no assignments is valid and still creates a row.
- Array-form assignments use `min(count, len(columnNames), len(columnValues))`; if that effective count is `<= 0`, no assignments are performed and the row is still added.
- Integer writes to `int8` / `int16` / `int32` columns are clamped to the destination range.
- Column lookup follows `DataTable` rules and is case-insensitive in practice. Guard quirk: only the exact lowercase name `id` is blocked; case variants such as `ID` still resolve to the primary-key column and can overwrite it.
- If an error occurs during assignment, the new row is not added because insertion happens only after all assignments finish.

**Errors & validation**
- Runtime error if a named column does not exist.
- Runtime error if a supplied value type does not match the destination column type.

**Examples**
- `id = DT_ROW_ADD("db", "name", "Alice")`

**Progress state**
- complete
