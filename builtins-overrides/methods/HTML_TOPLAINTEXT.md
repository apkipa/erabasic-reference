**Summary**
- Converts an HTML string to plain text by removing tags and expanding character references.

**Tags**
- string

**Syntax**
- `HTML_TOPLAINTEXT(html)`

**Arguments**
- `html`: string expression interpreted as an HTML string.

**Signatures / argument rules**
- Signature: `string HTML_TOPLAINTEXT(string html)`.

**Semantics**
- Removes all tag-like regions of the form `<...>` (including button tags and comments).
- Then expands character references in the remaining text (e.g. `&amp;` → `&`, `&#x41;` → `A`).

**Errors & validation**
- Malformed character references in the remaining text are runtime errors (e.g. an `&...` sequence missing a terminating `;`).
- Unsupported numeric character reference values (outside `0 <= codePoint <= 0xFFFF`) are runtime errors.

**Examples**
```erabasic
PRINTFORMW %HTML_TOPLAINTEXT("<b>AAA</b><i><b>BBB</b></i><s>CCC</s>")%
; prints: AAABBBCCC
```

**Progress state**
- complete
