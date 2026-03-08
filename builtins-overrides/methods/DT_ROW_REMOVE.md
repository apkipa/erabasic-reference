**Summary**
- Removes one or more rows from a named `DataTable` by `id`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_REMOVE(tableName, idValue)`
- `DT_ROW_REMOVE(tableName, idValues, count)`

**Signatures / argument rules**
- `DT_ROW_REMOVE(tableName, idValue)` → `long`
- `DT_ROW_REMOVE(tableName, idValues, count)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `idValue` (int): single primary-key value to remove.
- `idValues` (int[]): source array of primary-key values in the bulk form.
- `count` (int): requested number of `idValues` elements to consider.

**Semantics**
- If the table does not exist, returns `-1`.
- Single-row form removes the row whose primary key equals `idValue`, returning `1` on success or `0` if that row does not exist.
- Array form uses `min(count, len(idValues))`; if that effective count is `<= 0`, returns `0`.
- Array form builds an `id IN (...)` selection from that prefix and removes every matching row, returning the number of removed rows.
- Duplicate ids in the input array do not produce duplicate removals because selection happens through a single `IN (...)` query.

**Errors & validation**
- Runtime error if the generated `id IN (...)` selection is rejected by the underlying `DataTable` expression engine.

**Examples**
- `DT_ROW_REMOVE("db", id)`

**Progress state**
- complete
