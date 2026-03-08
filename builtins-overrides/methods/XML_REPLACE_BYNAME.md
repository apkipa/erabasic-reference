**Summary**
- Replaces selected nodes in a stored XML document with a new XML element.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REPLACE_BYNAME(xmlName, xpath, newXml [, setAllNodes])`

**Signatures / argument rules**
- `XML_REPLACE_BYNAME(xmlName, xpath, newXml)` → `long`
- `XML_REPLACE_BYNAME(xmlName, xpath, newXml, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects replacement targets.
- `newXml` (string): XML text whose document element becomes the replacement node.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero replaces all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `setAllNodes`, and multi-match node-reuse rules as the three-/four-argument form of `XML_REPLACE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `newXml` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REPLACE_BYNAME("menu", "/root/item", "<other/>", 1)`

**Progress state**
- complete
