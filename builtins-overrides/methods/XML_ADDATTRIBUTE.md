**Summary**
- Creates an XML attribute and inserts it at positions selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName [, attrValue [, methodType [, setAllNodes]]])`
- `XML_ADDATTRIBUTE(xmlVar, xpath, attrName [, attrValue [, methodType [, setAllNodes]]])`

**Signatures / argument rules**
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName)` → `long`
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName, attrValue)` → `long`
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName, attrValue, methodType)` → `long`
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName, attrValue, methodType, setAllNodes)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName, attrValue)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName, attrValue, methodType)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName, attrValue, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects insertion targets.
- `attrName` (string): attribute name to create.
- `attrValue` (optional, string; default `""`): attribute value.
- `methodType` (optional, int; default `0`): `0` append to the matched element, `1` insert before the matched attribute, `2` insert after the matched attribute; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`.
- Returns the full match count from `xpath`.
- Method `0` is for matched element nodes. Methods `1` and `2` are for matched attribute nodes.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, insertion is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no insertion occurs even though the match count is still returned.
- Multi-match quirk: one attribute object is reused for every successful insertion; it is not cloned per target. Each later insertion moves it again, so the final document retains it only at the last successful target.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Method `0` on non-element targets and other unsupported target kinds follow the underlying XML API failure path.

**Examples**
- `XML_ADDATTRIBUTE(0, "/root/item", "id", "42")`

**Progress state**
- complete
