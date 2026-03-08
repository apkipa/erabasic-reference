**Summary**
- Removes attributes selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REMOVEATTRIBUTE(xmlId, xpath [, setAllNodes])`
- `XML_REMOVEATTRIBUTE(xmlVar, xpath [, setAllNodes])`

**Signatures / argument rules**
- `XML_REMOVEATTRIBUTE(xmlId, xpath)` → `long`
- `XML_REMOVEATTRIBUTE(xmlId, xpath, setAllNodes)` → `long`
- `XML_REMOVEATTRIBUTE(ref xmlVar, xpath)` → `long`
- `XML_REMOVEATTRIBUTE(ref xmlVar, xpath, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects removal targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero removes all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`.
- Returns the full match count from `xpath`.
- This form is for attribute nodes; a single non-attribute match returns `0` instead of removing anything.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one attribute matches, it is removed regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no attribute is removed even though the match count is still returned.
- If more than one node matches and `setAllNodes != 0`, removal is attempted for every matched node; per-node failures in that loop do not change the returned count.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REMOVEATTRIBUTE(0, "/root/item/@id", 1)`

**Progress state**
- complete
