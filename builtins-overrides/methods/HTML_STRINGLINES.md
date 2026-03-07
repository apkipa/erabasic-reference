**Summary**
- Returns how many lines an HTML string would occupy when repeatedly split by a given width (using `HTML_SUBSTRING`).

**Tags**
- io

**Syntax**
- `HTML_STRINGLINES(html, width)`

**Signatures / argument rules**
- Signature: `int HTML_STRINGLINES(string html, int width)`.

**Arguments**
- `html` (string): HTML string.
- `width` (int): width in half-width character units.

**Semantics**
- If `html` is null/empty, returns `0`.
- Otherwise, repeatedly applies the same splitting rules as `HTML_SUBSTRING(html, width)`:
  - Each split consumes the prefix as one line.
  - The remainder becomes the next input.
- Returns the number of iterations until the remainder becomes empty.
- Compatibility notes:
  - This function inherits all parsing/splitting quirks from `HTML_SUBSTRING`, including case-sensitive special handling of `<br>`, `<img ...>`, and `<shape ...>`.

**Errors & validation**
- Invalid HTML strings (including invalid character references) may raise runtime errors.

**Examples**
```erabasic
PRINTVL HTML_STRINGLINES("AB<b>CD</b>", 4)
```

**Progress state**
- complete
