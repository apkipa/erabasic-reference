**Summary**
- Removes a stored XML document by key.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_RELEASE(xmlId)`

**Signatures / argument rules**
- `XML_RELEASE(xmlId)` → `long`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.

**Semantics**
- If a document exists for the resolved key, it is removed and the function returns `1`.
- If no document exists for that key, the function returns `0`.

**Errors & validation**
- None.

**Examples**
- `XML_RELEASE(0)`

**Progress state**
- complete
