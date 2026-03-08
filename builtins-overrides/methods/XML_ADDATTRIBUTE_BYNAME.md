**Summary**
- Creates an XML attribute and inserts it into a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName [, attrValue [, methodType [, setAllNodes]]])`

**Signatures / argument rules**
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName)` → `long`
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName, attrValue)` → `long`
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName, attrValue, methodType)` → `long`
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName, attrValue, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects insertion targets.
- `attrName` (string): attribute name to create.
- `attrValue` (optional, string; default `""`): attribute value.
- `methodType` (optional, int; default `0`): `0` append to the matched element, `1` insert before the matched attribute, `2` insert after the matched attribute; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, target-kind, and multi-match attribute-reuse rules as `XML_ADDATTRIBUTE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_ADDATTRIBUTE_BYNAME("menu", "/root/item", "id", "42")`

**Progress state**
- complete
