**Summary**
- Updates option metadata for an existing data-table column.

**Tags**
- data

**Syntax**
- `DT_COLUMN_OPTIONS <dataTableName>, <columnName>, DEFAULT, <optionValue>`
- `DT_COLUMN_OPTIONS <dataTableName>, <columnName>, DEFAULT, <optionValue>, DEFAULT, <optionValue>, ...`

**Arguments**
- `<dataTableName>` (string): data-table name.
- `<columnName>` (string): column name.
- `DEFAULT` (option keyword): matched case-insensitively.
- `<optionValue>` (same type as the column): default value to store for that option.
  - String columns require a string value.
  - Numeric columns require an int value.

**Semantics**
- Requires an existing data table and an existing column.
- Currently the only supported option keyword is `DEFAULT`.
- `DEFAULT` changes the column’s default value used for future row/cell operations that consult the column default.
- If a numeric column uses a narrower integer type than the script value type, the stored default is converted with the same clamping rules as other data-table numeric writes.
- Repeated option pairs are processed left-to-right; a later `DEFAULT` overrides an earlier one.

**Errors & validation**
- Parse / argument-validation error if the first two arguments are missing, if an option keyword has no following value, or if an unknown option keyword is used.
- Runtime error if the named table or column does not exist.
- Runtime error if `<optionValue>` has the wrong type for the column.

**Examples**
- `DT_COLUMN_OPTIONS "SHOP", "PRICE", DEFAULT, 0`
- `DT_COLUMN_OPTIONS "SHOP", "NAME", DEFAULT, "(none)"`

**Progress state**
- complete
