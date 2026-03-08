**Summary**
- Assigns a string to selected XML nodes.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_SET(xmlId, xpath, value [, setAllNodes [, outputType]])`
- `XML_SET(xmlVar, xpath, value [, setAllNodes [, outputType]])`

**Signatures / argument rules**
- `XML_SET(xmlId, xpath, value)` → `long`
- `XML_SET(xmlId, xpath, value, setAllNodes)` → `long`
- `XML_SET(xmlId, xpath, value, setAllNodes, outputType)` → `long`
- `XML_SET(ref xmlVar, xpath, value)` → `long`
- `XML_SET(ref xmlVar, xpath, value, setAllNodes)` → `long`
- `XML_SET(ref xmlVar, xpath, value, setAllNodes, outputType)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): XPath expression evaluated against the selected document.
- `value` (string): replacement text.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero updates all of them; `0` leaves them all unchanged.
- `outputType` (optional, int; default `0`): write mode; `0` = `Value`, `1` = `InnerText`, `2` = `InnerXml`; other values clamp to `0`.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution:
- `XML_SET(xmlId, ...)` mutates a stored document in place,
- `XML_SET(ref xmlVar, ...)` reparses the variable as XML, applies the mutation to that temporary document, and writes back `OuterXml` only when at least one node matches.
- Returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, that node is always updated.
- If more than one node matches and `setAllNodes == 0`, no node is updated even though the match count is still returned.
- If more than one node matches and `setAllNodes != 0`, every matched node is updated.
- Style `0` writes `XmlNode.Value`; on element nodes that follows .NET element-value rules and raises a runtime error instead of writing text.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` does not contain well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Runtime error if the chosen write mode is invalid for the matched node type.

**Examples**
- `XML_SET(0, "/root/a/@id", "42")`

**Progress state**
- complete
