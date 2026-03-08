**Summary**
- Deletes a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_RELEASE(tableName)`

**Signatures / argument rules**
- `DT_RELEASE(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table exists, it is removed.
- The function always returns `1`, even when the table was already absent.

**Errors & validation**
- None.

**Examples**
- `DT_RELEASE("db")`

**Progress state**
- complete
