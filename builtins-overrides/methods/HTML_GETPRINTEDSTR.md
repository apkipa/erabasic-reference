**Summary**
- Returns the HTML-formatted representation of a previously displayed **logical output line**.

**Tags**
- io

**Syntax**
- `HTML_GETPRINTEDSTR(<lineNo>)`

**Arguments**
- `<lineNo>` (optional): integer expression. Defaults to `0`.
  - `0` = the most recent logical output line.
  - `1` = the second most recent logical output line.
  - And so on.

- Omitted arguments / defaults:
  - `<lineNo>` defaults to `0`.

**Signatures / argument rules**
- Signature: `string HTML_GETPRINTEDSTR(int lineNo = 0)`.
- `<lineNo>` is evaluated as an integer expression.

**Semantics**
- Interprets `<lineNo>` as a non-negative index into the current display log’s **logical lines**, counted from the end:
  - `HTML_GETPRINTEDSTR(0)` returns the most recently produced logical output line.
- Returns `""` if the requested line does not exist.
- The returned HTML is a normalized representation of the displayed line:
  - It always wraps the line in `<p align='...'><nobr> ... </nobr></p>`.
  - It uses `<br>` between display-wrapped lines within the same logical line.
  - Button segments are represented with `<button ...>` / `<nonbutton ...>` tags (including `title` and `pos` when present).
  - Inline images and shapes are represented by their tag-like alt text (e.g. `<img ...>` / `<shape ...>`).
  - `<div ...>` sub-area elements are omitted.
- This function does not modify the display.

**Errors & validation**
- If `<lineNo> < 0`, this is a runtime error.

**Examples**
```erabasic
PRINTL "Hello"
PRINTL "World"

; Gets the most recent logical line (the "World" line)
S = HTML_GETPRINTEDSTR(0)
```

**Progress state**
- complete
