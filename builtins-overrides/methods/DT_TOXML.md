**Summary**
- Serializes a named `DataTable` to XML and also exposes its schema XML.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_TOXML(tableName)`
- `DT_TOXML(tableName, schemaOutput)`

**Signatures / argument rules**
- `DT_TOXML(tableName)` → `string`
- `DT_TOXML(tableName, schemaOutput)` → `string`

**Arguments**
- `tableName` (string): table identifier.
- `schemaOutput` (optional, string variable): destination for schema XML; if omitted, schema is written to `RESULTS:1`.

**Semantics**
- If the table does not exist, returns `""`.
- On success, returns the data XML produced by `DataTable.WriteXml(...)`.
- Also writes the schema XML produced by `DataTable.WriteXmlSchema(...)`.
- If `schemaOutput` is omitted, that schema string is written to `RESULTS:1`; `RESULTS:0` is not used for this function.

**Errors & validation**
- None.

**Examples**
- `data '= DT_TOXML("db", schema)`

**Progress state**
- complete
