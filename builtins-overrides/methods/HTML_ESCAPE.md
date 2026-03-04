**Summary**
- Escapes a plain-text string for use in HTML strings.

**Tags**
- string

**Syntax**
- `HTML_ESCAPE(text)`

**Arguments**
- `text`: string expression.

**Signatures / argument rules**
- Signature: `string HTML_ESCAPE(string text)`.

**Semantics**
- Replaces:
  - `&` → `&amp;`
  - `>` → `&gt;`
  - `<` → `&lt;`
  - `"` → `&quot;`
  - `'` → `&apos;`
- All other characters are unchanged.

**Errors & validation**
- None.

**Examples**
```erabasic
PRINTFORMW %HTML_ESCAPE("A&B<C>D'E")%
; prints: A&amp;B&lt;C&gt;D&apos;E
```

**Progress state**
- complete
