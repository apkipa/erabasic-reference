**Summary**
- Returns the HTML-formatted representation of one currently visible **logical output line** in the normal output area.

**Tags**
- io

**Syntax**
- `HTML_GETPRINTEDSTR()`
- `HTML_GETPRINTEDSTR(<lineNo>)`

**Signatures / argument rules**
- Signature: `string HTML_GETPRINTEDSTR(int lineNo = 0)`.
- `<lineNo>` is evaluated as an integer expression.

**Arguments**
- `<lineNo>` (optional, int; default `0`): zero-based index from the newest visible logical line backward.
  - `0` = the most recent currently visible logical output line.
  - `1` = the second most recent currently visible logical output line.
  - Larger values continue counting backward through the currently visible logical lines.

**Semantics**
- Interprets `<lineNo>` as a non-negative index into the current visible **logical-line** history of the normal output area.
- Returns `""` if the requested logical line does not exist.
- The returned HTML is a normalized representation of that visible logical line:
  - it always wraps the line in `<p align='...'><nobr> ... </nobr></p>`,
  - it uses `<br>` between display rows that belong to the same logical line,
  - button segments are represented with `<button ...>` / `<nonbutton ...>` tags (including `title` and `pos` when present),
  - inline images and shapes are represented by their tag-like alt text (for example `<img ...>` / `<shape ...>`),
  - `<div ...>` sub-area elements are omitted.
- This function does not modify the display.
- Layer boundary:
  - pending buffered output is not included,
  - the `HTML_PRINT_ISLAND` layer is not included,
  - while a temporary line remains visible, it can be returned here like any other visible logical line.

**Errors & validation**
- Runtime error if `<lineNo> < 0`.

**Examples**
```erabasic
PRINTL "Hello"
PRINTL "World"
S = HTML_GETPRINTEDSTR(0)
```

**Progress state**
- complete
