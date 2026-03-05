**Summary**
- Prints an HTML string (Emuera’s HTML-like mini language) as console output.

**Tags**
- io

**Syntax**
- `HTML_PRINT <html> [, <toBuffer>]`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<toBuffer>` (optional, int; default `0`)
  - `0` (default): print as a complete logical output line (implicit line end).
  - non-zero: append the HTML output into the current print buffer (no implicit line end).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string.
  - If it is null/empty, no output is produced.
- Interprets the string as an HTML string and renders it according to `html-output.md` (tags, entities, comments, wrapping rules).
- If `<toBuffer> = 0` (or omitted):
  - Any pending print buffer content is flushed first (as with other “line-ending” print operations).
  - The HTML is rendered into one logical output line (it may still occupy multiple display lines due to `<br>` or wrapping).
- If `<toBuffer> != 0`:
  - The HTML is converted to output segments and appended into the current print buffer.
  - `<br>` (and literal `'\n'` inside the HTML string) insert display line breaks, but no final line end is implied.
- The output is not affected by non-HTML text style commands like `ALIGNMENT`, `SETFONT`, `SETCOLOR`, or `FONTSTYLE`; use HTML tags (`<p>`, `<font>`, `<b>`, etc.) instead.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (unsupported tags, invalid attributes, invalid character references, tag structure violations), except where a tag explicitly specifies a fallback-to-text behavior (e.g. unresolved `<img>` resources).

**Examples**
```erabasic
; Prints one logical line (with HTML styling)
HTML_PRINT "<p align='center'><b>Hello</b> <font color='red'>world</font></p>"
```

```erabasic
; Appends into the current print buffer (no implicit newline)
HTML_PRINT "<b>HP:</b> 10", 1
PRINTL ""
```

**Progress state**
- complete
