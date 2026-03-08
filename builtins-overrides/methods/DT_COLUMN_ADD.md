**Summary**
- Adds a column to a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_ADD(tableName, columnName [, type [, nullable]])`

**Signatures / argument rules**
- `DT_COLUMN_ADD(tableName, columnName)` → `long`
- `DT_COLUMN_ADD(tableName, columnName, type)` → `long`
- `DT_COLUMN_ADD(tableName, columnName, type, nullable)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (string): column name.
- `type` (optional, int|string): column type.
  - Integer codes: `1=int8`, `2=int16`, `3=int32`, `4=int64`, `5=string`.
  - String names: exact lowercase `int8`, `int16`, `int32`, `int64`, or `string`.
- `nullable` (optional, int; default `1`): non-zero allows `NULL`; `0` disallows it.

**Semantics**
- If the table does not exist, returns `-1`.
- Column-name collisions are checked through `DataTable` column lookup, so case variants such as `id` and `ID` count as the same existing column.
- If the column already exists, returns `0`.
- If `type` is omitted, the new column uses `string` type.
- Otherwise creates the column and returns `1`.

**Errors & validation**
- Runtime error if `type` is present but not one of the supported integer codes or exact lowercase type names.

**Examples**
- `DT_COLUMN_ADD("db", "name")`

**Progress state**
- complete
