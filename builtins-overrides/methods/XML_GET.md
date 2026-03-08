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
- Third-argument dispatch is type-based: omitted or integer `0` writes nothing; non-zero integer copies projected values to `RESULTS` starting at index `0`; `outputArray` copies there instead.
- In the array-output form, `outputType` occupies the fourth slot rather than the third.
- Projection styles are: `0` or other value = `Value`, `1` = `InnerText`, `2` = `InnerXml`, `3` = `OuterXml`, `4` = `Name`.
- Style `0` reads `XmlNode.Value`. On element nodes, that value is `null`. Use `outputType = 1` (`InnerText`) if you want the element's text content.
- Copies start at destination index `0` and stop when the destination fills. Excess matches are ignored; untouched slots are not cleared. The return value remains the full match count.

**Errors & validation**
- Returns `-1` if integer-key lookup is requested and no stored document exists for that key.
- Runtime error if raw-XML parsing fails.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_GET("<root><a>1</a></root>", "/root/a", 1, 1)`

**Progress state**
- complete
