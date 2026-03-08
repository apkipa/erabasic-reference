**Summary**
- Assigns a string to selected nodes in a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_SET_BYNAME(xmlName, xpath, value [, setAllNodes [, outputType]])`

**Signatures / argument rules**
- `XML_SET_BYNAME(xmlName, xpath, value)` → `long`
- `XML_SET_BYNAME(xmlName, xpath, value, setAllNodes)` → `long`
- `XML_SET_BYNAME(xmlName, xpath, value, setAllNodes, outputType)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): XPath expression evaluated against the stored document.
- `value` (string): replacement text.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero updates all of them; `0` leaves them all unchanged.
- `outputType` (optional, int; default `0`): write mode; `0` = `Value`, `1` = `InnerText`, `2` = `InnerXml`; other values clamp to `0`.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `setAllNodes`, and write-mode rules as `XML_SET`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.
- Runtime error if the chosen write mode is invalid for the matched node type.

**Examples**
- `XML_SET_BYNAME("menu", "/root/a/@id", "42")`

**Progress state**
- complete
