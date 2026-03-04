**Summary**
- Returns (and clears) the current pending print buffer as an HTML string.

**Tags**
- io

**Syntax**
- `HTML_POPPRINTINGSTR()`

**Arguments**
- None.

**Signatures / argument rules**
- Signature: `string HTML_POPPRINTINGSTR()`.

**Semantics**
- If the engine output is disabled or the print buffer is empty, returns `""`.
- Otherwise:
  - Flushes the current print buffer into display-line structures **without displaying them**.
  - Clears the print buffer.
  - Converts the flushed content to an HTML string and returns it.
- The returned HTML:
  - uses `<br>` between display-wrapped lines within the flushed buffer
  - does **not** include `<p ...>` or `<nobr>` wrappers (so it does not reflect `ALIGNMENT`).
  - omits `<div ...>` sub-area elements

**Errors & validation**
- None.

**Examples**
```erabasic
PRINT "A"
PRINT "B"
S = HTML_POPPRINTINGSTR()
; At this point, the pending buffer is cleared and nothing was displayed.
```

**Progress state**
- complete
