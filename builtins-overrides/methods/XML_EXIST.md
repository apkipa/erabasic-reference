**Summary**
- Checks whether a stored XML document exists.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_EXIST(xmlId)`

**Signatures / argument rules**
- `XML_EXIST(xmlId)` → `long`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.

**Semantics**
- Returns `1` if a stored document exists for the resolved key.
- Returns `0` otherwise.

**Errors & validation**
- None.

**Examples**
- `IF XML_EXIST("menu")`

**Progress state**
- complete
