**Summary**
- Selects XML nodes and optionally copies their projected values to a string array.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_GET(xmlOrId, xpath [, doOutput [, outputType]])`
- `XML_GET(xmlOrId, xpath, outputArray [, outputType])`

**Signatures / argument rules**
- `XML_GET(xmlOrId, xpath)` → `long`
- `XML_GET(xmlOrId, xpath, doOutput)` → `long`
- `XML_GET(xmlOrId, xpath, doOutput, outputType)` → `long`
- `XML_GET(xmlOrId, xpath, ref outputArray)` → `long`
- `XML_GET(xmlOrId, xpath, ref outputArray, outputType)` → `long`

**Arguments**
- `xmlOrId` (int|string): integer values resolve a stored document by decimal-string key; string values in this non-`_BYNAME` form are parsed as raw XML text for this call.
- `xpath` (string): XPath expression evaluated against the selected document.
- `doOutput` (optional, int; default `0`): non-zero copies to `RESULTS`; `0` leaves outputs untouched.
- `outputType` (optional, int; default `0`): projection style.
- `outputArray` (string[]): destination array for copied values.

**Semantics**
- Selects nodes with `xpath` and returns the full match count.
- Output destination rules:
- if the third argument is omitted or is integer `0`, nothing is written,
- if the third argument is a non-zero integer, matched values are copied to `RESULTS` starting at index `0`,
- if the third argument is `ref outputArray`, matched values are copied there instead.
- `outputType` mapping:
- `1`: `InnerText`,
- `2`: `InnerXml`,
- `3`: `OuterXml`,
- `4`: `Name`,
- other values or omission: `Value`.
- Style `0`/default reads `XmlNode.Value`; for element nodes that is `null`, not the element's text content.
- Copies at most the destination length, does not clear untouched slots, and still returns the total match count rather than the copied count.

**Errors & validation**
- Returns `-1` if integer-key lookup is requested and no stored document exists for that key.
- Runtime error if raw-XML parsing fails.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_GET("<root><a>1</a></root>", "/root/a", 1, 1)`

**Progress state**
- complete
