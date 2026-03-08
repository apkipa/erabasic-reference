**Summary**
- Edits an existing row in a named `DataTable` selected by `id`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_SET(tableName, idValue [, columnName, columnValue] ...)`
- `DT_ROW_SET(tableName, idValue, columnNames, columnValues, count)`

**Signatures / argument rules**
- `DT_ROW_SET(tableName, idValue)` → `long`
- `DT_ROW_SET(tableName, idValue, columnName, columnValue [, columnName, columnValue] ...)` → `long`
- `DT_ROW_SET(tableName, idValue, columnNames, columnValues, count)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `idValue` (int): primary-key value of the row to edit.
- `columnName` (optional, string): column name in the variadic pair form.
- `columnValue` (optional, int|string): value in the variadic pair form; its type must match the destination column type.
- `columnNames` (string[]): column names in the array form.
- `columnValues` (int[]|string[]): homogeneous value array in the array form; mixed string/integer array input is not supported.
- `count` (int): requested number of array-form assignments.

**Semantics**
- If the table does not exist, returns `-1`.
- If no row exists with primary-key `idValue`, returns `-2`.
- Returns the number of assignments actually performed.
- Array-form assignments use `min(count, len(columnNames), len(columnValues))`; if that effective count is `<= 0`, returns `0` without changing the row.
- Integer writes to `int8` / `int16` / `int32` columns are clamped to the destination range.
- Column lookup follows `DataTable` rules and is case-insensitive in practice. Guard quirk: only the exact lowercase name `id` is blocked; case variants such as `ID` still resolve to the primary-key column and can overwrite it.
- Assignments are applied sequentially to the already-existing row, so earlier writes remain visible if a later write throws a runtime error.

**Errors & validation**
- Runtime error if a named column does not exist.
- Runtime error if a supplied value type does not match the destination column type.

**Examples**
- `DT_ROW_SET("db", id, "age", 18)`

**Progress state**
- complete
