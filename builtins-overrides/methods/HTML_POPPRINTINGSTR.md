**Summary**
- Returns (and clears) the current pending print buffer as an HTML string.

**Tags**
- io

**Syntax**
- `HTML_POPPRINTINGSTR()`

**Signatures / argument rules**
- Signature: `string HTML_POPPRINTINGSTR()`.

**Arguments**
- None.

**Semantics**
- If output is disabled or the pending print buffer is empty, returns `""`.
- Otherwise:
  - converts the current pending print buffer into the same internal display-line structures that normal flushing would use,
  - clears the pending print buffer,
  - returns the converted content as HTML,
  - does **not** append that content to the visible normal output area.
- The returned HTML:
  - preserves structured button/nonbutton regions,
  - uses `<br>` between internal display-row breaks within the flushed buffer,
  - does **not** include outer `<p ...>` / `<nobr>` wrappers, so `ALIGNMENT` is not reflected,
  - omits `<div ...>` sub-area elements.
- Layer boundary:
  - this reads the pending print buffer,
  - it does not read committed visible history,
  - it does not read the `HTML_PRINT_ISLAND` layer.

**Errors & validation**
- None.

**Examples**
```erabasic
PRINT A
PRINTBUTTON "[B]", "B"
S = HTML_POPPRINTINGSTR()
; The buffer is now cleared and nothing was added to visible output.
```

**Progress state**
- complete
