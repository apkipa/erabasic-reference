**Summary**
- Runs a `DataTable.Select(...)` query and outputs matching row ids.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_SELECT(tableName [, filterExpression [, sortRule [, outputArray]]])`

**Signatures / argument rules**
- `DT_SELECT(tableName)` → `long`
- `DT_SELECT(tableName, filterExpression)` → `long`
- `DT_SELECT(tableName, filterExpression, sortRule)` → `long`
- `DT_SELECT(tableName, filterExpression, sortRule, outputArray)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `filterExpression` (optional, string): `DataTable.Select` filter expression; omission selects every row.
- `sortRule` (optional, string): `DataTable.Select` sort rule; omission leaves the default order unchanged.
- `outputArray` (optional, int[]): destination array for row ids; if omitted, `RESULT` is used instead.

**Semantics**
- If the table does not exist, returns `-1`.
- Delegates filtering and sorting directly to `DataTable.Select(...)`.
- The returned row ids are the values of the table's first column, which is the auto-created `id` primary key.
- If `outputArray` is omitted, copied ids go to `RESULT:1`, `RESULT:2`, ... and `RESULT:0` is set to the full match count.
- If `outputArray` is supplied, copied ids go to that array starting at index `0`; `RESULT` is not updated by this path.
- Copies row ids until the destination fills. In the `RESULT` form, index `0` stores the count, so at most `length - 1` ids are copied. Untouched slots are not cleared. The return value remains the full match count.
- The function return value is always the full match count, not the copied count.
- Explicitly omitted middle arguments remain omitted; for example, supplying only `sortRule` requires an omitted `filterExpression` slot.

**Errors & validation**
- Runtime error if `filterExpression` or `sortRule` is rejected by the underlying `DataTable.Select` parser.

**Examples**
- `count = DT_SELECT("db", "age >= 18", "age ASC", ids)`

**Progress state**
- complete
