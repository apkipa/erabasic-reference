**Summary**
- Removes attributes selected by XPath from a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REMOVEATTRIBUTE_BYNAME(xmlName, xpath [, setAllNodes])`

**Signatures / argument rules**
- `XML_REMOVEATTRIBUTE_BYNAME(xmlName, xpath)` → `long`
- `XML_REMOVEATTRIBUTE_BYNAME(xmlName, xpath, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects removal targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero removes all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count and target-kind rules as `XML_REMOVEATTRIBUTE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REMOVEATTRIBUTE_BYNAME("menu", "/root/item/@id", 1)`

**Progress state**
- complete
