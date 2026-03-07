**Summary**
- Appends HTML-rendered rows into the separate `HTML_PRINT_ISLAND` layer rather than the normal output/log model.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND <html>`
- `HTML_PRINT_ISLAND <html>, <ignored>`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<ignored>` (optional, int): compatibility-only argument.
  - If provided, it must parse/type-check as an `int` expression.
  - Its value is ignored at runtime.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string and parses it with the same HTML mini-language used by `HTML_PRINT`.
- Appends the resulting display rows to the retained `HTML_PRINT_ISLAND` layer in order.
  - `<br>` and literal `\n` create separate appended island rows.
  - Automatic wrapping can also create additional appended island rows.
- Layer boundary:
  - the island layer is not part of the normal display-line array,
  - it is not counted by `LINECOUNT`,
  - it is not removed by `CLEARLINE`,
  - it is not returned by `GETDISPLAYLINE` or `HTML_GETPRINTEDSTR`.
- Painting model:
  - island rows are painted from the top of the window downward,
  - they do not scroll together with the normal backlog.
- Repaint timing:
  - this instruction updates island-layer state immediately,
  - but it does not itself force an immediate repaint,
  - so the changed island content becomes visible on the next repaint allowed/forced by the redraw schedule.
- `<div ...>` sub-area elements are not rendered in the island layer.
- Use `HTML_PRINT_ISLAND_CLEAR` to clear the island layer.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
HTML_PRINT_ISLAND "<font color='white'>Status</font><br>HP: 10"
```

**Progress state**
- complete
