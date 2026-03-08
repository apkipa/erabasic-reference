**Summary**
- Creates a stored XML document under a key.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_DOCUMENT(xmlId, xmlContent)`

**Signatures / argument rules**
- `XML_DOCUMENT(xmlId, xmlContent)` → `long`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.
- `xmlContent` (string): XML text to parse and store.

**Semantics**
- Uses the process-local stored-document table shared by the `XML_*` built-ins.
- If a document already exists for the resolved key, returns `0` and leaves that document unchanged.
- Otherwise parses `xmlContent`, stores the resulting document under the key, and returns `1`.

**Errors & validation**
- Runtime error if `xmlContent` is not well-formed XML.

**Examples**
- `XML_DOCUMENT("menu", "<root/>")`

**Progress state**
- complete
