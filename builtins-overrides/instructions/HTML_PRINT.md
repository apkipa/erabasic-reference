**Summary**
- Prints an HTML string (Emuera’s HTML-like mini language) into the normal output model.

**Tags**
- io

**Syntax**
- `HTML_PRINT <html> [, <toBuffer>]`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<toBuffer>` (optional, int; default `0`)
  - `0` (default): append directly to the visible normal output area as one logical line.
  - non-zero: append the parsed HTML segments to the pending print buffer (no immediate visible line append).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string.
  - If it is null/empty, no output is produced.
- Interprets the string as HTML according to `html-output.md`.
- If `<toBuffer> = 0` (or omitted):
  - any pending print-buffer content is flushed first as normal visible output,
  - the HTML output is then appended directly to the visible normal output area,
  - the entire `HTML_PRINT` call constitutes one logical line, even if it occupies multiple visible display rows because of `<br>` or wrapping.
- If `<toBuffer> != 0`:
  - the HTML output is converted to output segments and appended to the pending print buffer,
  - `<br>` (and literal `\n` inside the HTML string) create internal display-row breaks for the future flush,
  - but no visible line is appended yet and no final logical-line end is implied.
- Style boundary:
  - non-HTML text style commands such as `ALIGNMENT`, `SETFONT`, `SETCOLOR`, or `FONTSTYLE` do not style the HTML output,
  - use HTML tags (`<p>`, `<font>`, `<b>`, etc.) instead.
- Layer boundary:
  - `HTML_PRINT(..., 0)` affects the normal visible output area,
  - `HTML_PRINT(..., nonZero)` affects only the pending print buffer until some later flush/line-end operation.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (unsupported tags, invalid attributes, invalid character references, or invalid tag structure), except where a tag explicitly defines fallback-to-text behavior.

**Examples**
```erabasic
HTML_PRINT "<p align='center'><b>Hello</b> <font color='red'>world</font></p>"
```

```erabasic
HTML_PRINT "<b>HP:</b> 10", 1
PRINTL ""
```

**Progress state**
- complete
