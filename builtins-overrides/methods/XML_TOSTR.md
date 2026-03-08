**Summary**
- Returns the serialized text of a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_TOSTR(xmlId)`

**Signatures / argument rules**
- `XML_TOSTR(xmlId)` → `string`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.

**Semantics**
- If a stored document exists for the resolved key, returns its current `OuterXml`.
- If no stored document exists for that key, returns `""`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORM %XML_TOSTR("menu")%`

**Progress state**
- complete
