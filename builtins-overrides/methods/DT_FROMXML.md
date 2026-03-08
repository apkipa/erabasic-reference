**Summary**
- Loads a named `DataTable` from schema XML plus data XML.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_FROMXML(tableName, schemaXml, dataXml)`

**Signatures / argument rules**
- `DT_FROMXML(tableName, schemaXml, dataXml)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `schemaXml` (string): schema XML consumed by `ReadXmlSchema(...)`.
- `dataXml` (string): data XML consumed by `ReadXml(...)`.

**Semantics**
- Builds a fresh `DataTable`, reads `schemaXml`, then reads `dataXml` into it.
- If both reads succeed, replaces the existing named table or creates a new one and returns `1`.
- If any step fails, returns `0` and leaves the previously stored table unchanged.

**Errors & validation**
- None; all load/parse failures collapse to return value `0`.

**Examples**
- `DT_FROMXML("db", schema, data)`

**Progress state**
- complete
