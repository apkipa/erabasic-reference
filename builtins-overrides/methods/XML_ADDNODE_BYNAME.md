**Summary**
- Inserts an XML element parsed from text into a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml [, methodType [, setAllNodes]])`

**Signatures / argument rules**
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml)` → `long`
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml, methodType)` → `long`
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects insertion targets.
- `childXml` (string): XML text whose document element becomes the inserted node.
- `methodType` (optional, int; default `0`): `0` append as child, `1` insert before the matched node, `2` insert after the matched node; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `methodType`, and multi-match node-reuse rules as `XML_ADDNODE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `childXml` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_ADDNODE_BYNAME("menu", "/root/list", "<item/>")`

**Progress state**
- complete
