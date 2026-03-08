**Summary**
- Creates an empty named `DataTable` with an automatic primary-key column.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CREATE(tableName)`

**Signatures / argument rules**
- `DT_CREATE(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If a table with that name already exists, returns `0` and leaves it unchanged.
- Otherwise creates a new table with `CaseSensitive = true`, auto-adds an `id` column of type `int64`, marks it non-null / unique / primary-key, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `DT_CREATE("db")`

**Progress state**
- complete
