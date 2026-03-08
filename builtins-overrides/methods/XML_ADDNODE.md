**Summary**
- Inserts an XML element parsed from text at positions selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDNODE(xmlId, xpath, childXml [, methodType [, setAllNodes]])`
- `XML_ADDNODE(xmlVar, xpath, childXml [, methodType [, setAllNodes]])`

**Signatures / argument rules**
- `XML_ADDNODE(xmlId, xpath, childXml)` → `long`
- `XML_ADDNODE(xmlId, xpath, childXml, methodType)` → `long`
- `XML_ADDNODE(xmlId, xpath, childXml, methodType, setAllNodes)` → `long`
- `XML_ADDNODE(ref xmlVar, xpath, childXml)` → `long`
- `XML_ADDNODE(ref xmlVar, xpath, childXml, methodType)` → `long`
- `XML_ADDNODE(ref xmlVar, xpath, childXml, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects insertion targets.
- `childXml` (string): XML text whose document element becomes the inserted node.
- `methodType` (optional, int; default `0`): `0` append as child, `1` insert before the matched node, `2` insert after the matched node; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`: stored-document lookup for `xmlId`, or parse / write-back behavior for `ref xmlVar`.
- Returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, insertion is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no insertion occurs even though the match count is still returned.
- Multi-match quirk: one inserted node is reused for every successful insertion; it is not cloned per target. Each later insertion moves it again, so the final document contains it only at the last successful target.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` or `childXml` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Single-target before/after insertion returns `0` if the matched node has no parent; other unsupported target kinds follow the underlying XML API failure path.

**Examples**
- `XML_ADDNODE(0, "/root/list", "<item/>")`

**Progress state**
- complete
