**Summary**
- Copies column names from a named `DataTable` to a string array.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_NAMES(tableName)`
- `DT_COLUMN_NAMES(tableName, outputArray)`

**Signatures / argument rules**
- `DT_COLUMN_NAMES(tableName)` → `long`
- `DT_COLUMN_NAMES(tableName, outputArray)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `outputArray` (optional, string[]): destination array; if omitted, `RESULTS` is used.

**Semantics**
- If the table does not exist, returns `-1`.
- Copies names in column order starting at destination index `0` and returns the full column count.
- The auto-created `id` column is included.
- No destination clearing is performed.

**Errors & validation**
- Runtime error if the destination array is shorter than the column count; this build does not clamp the copy length here.

**Examples**
- `DT_COLUMN_NAMES("db", names)`

**Progress state**
- complete
