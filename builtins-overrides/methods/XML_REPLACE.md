**Summary**
- Replaces either an entire stored XML document or selected nodes with a new XML element.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REPLACE(xmlId, newXml)`
- `XML_REPLACE(xmlId, xpath, newXml [, setAllNodes])`
- `XML_REPLACE(xmlVar, xpath, newXml [, setAllNodes])`

**Signatures / argument rules**
- `XML_REPLACE(xmlId, newXml)` → `long`
- `XML_REPLACE(xmlId, xpath, newXml)` → `long`
- `XML_REPLACE(xmlId, xpath, newXml, setAllNodes)` → `long`
- `XML_REPLACE(ref xmlVar, xpath, newXml)` → `long`
- `XML_REPLACE(ref xmlVar, xpath, newXml, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int|string): in the two-argument form this is always a stored-document key; integer values are converted to decimal strings.
- `newXml` (string): XML text whose document element becomes the replacement node, or the whole new stored document in the two-argument form.
- `xpath` (string): selects replacement targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero replaces all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML for the three-/four-argument form.

**Semantics**
- Two-argument form: parses `newXml` and replaces the entire stored document for `xmlId`; raw XML variables are not accepted in this form.
- Three-/four-argument forms: target resolution matches `XML_SET`.
- Selected-node replacement returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, replacement is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no node is replaced even though the match count is still returned.
- Multi-match quirk: the engine constructs one replacement node and reuses it for every successful replacement instead of cloning it. Each later successful replacement moves that same node again, so only the last successful replacement remains in the final document.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `newXml` or `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Single-target replacement returns `0` when the matched node cannot be replaced because it has no parent.

**Examples**
- `XML_REPLACE(0, "/root/item", "<other/>", 1)`

**Progress state**
- complete
