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
- Uses stored-document lookup only; unlike `XML_GET`, this form never parses raw XML from the first argument.
- Otherwise follows the same projection, copy-limit, and return-value rules as `XML_GET`.
- Third-argument dispatch is type-based: omitted or integer `0` writes nothing; non-zero integer copies projected values to `RESULTS` starting at index `0`; `outputArray` copies there instead.
- In the array-output form, `outputType` occupies the fourth slot rather than the third.
- Projection styles are: `0` or other value = `Value`, `1` = `InnerText`, `2` = `InnerXml`, `3` = `OuterXml`, `4` = `Name`.
- Style `0` reads `XmlNode.Value`. On element nodes, that value is `null`. Use `outputType = 1` (`InnerText`) if you want the element's text content.
- Copies start at destination index `0` and stop when the destination fills. Excess matches are ignored; untouched slots are not cleared. The return value remains the full match count.

**Errors & validation**
- Returns `-1` if no stored document exists for the resolved key.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_GET_BYNAME("menu", "/root/a", 1, 1)`

**Progress state**
- complete
