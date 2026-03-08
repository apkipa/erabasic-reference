**Summary**
- Selects nodes from a stored XML document and optionally copies their projected values to a string array.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_GET_BYNAME(xmlName, xpath [, doOutput [, outputType]])`
- `XML_GET_BYNAME(xmlName, xpath, outputArray [, outputType])`

**Signatures / argument rules**
- `XML_GET_BYNAME(xmlName, xpath)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, doOutput)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, doOutput, outputType)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, ref outputArray)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, ref outputArray, outputType)` → `long`

**Arguments**
- `xmlName` (int|string): stored-document key; string values are used directly, and integer values are also accepted here and converted to decimal strings.
- `xpath` (string): XPath expression evaluated against the stored document.
- `doOutput` (optional, int; default `0`): non-zero copies to `RESULTS`; `0` leaves outputs untouched.
- `outputType` (optional, int; default `0`): projection style.
- `outputArray` (string[]): destination array for copied values.

**Semantics**
- Same projection, copy-limit, and return-value rules as `XML_GET`.
- Unlike `XML_GET`, this form never parses raw XML from the first argument; it always performs stored-document lookup.
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
- Returns `-1` if no stored document exists for the resolved key.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_GET_BYNAME("menu", "/root/a", 1, 1)`

**Progress state**
- complete
