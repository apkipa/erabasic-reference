**Summary**
- Prints an HTML string into the “HTML island” layer, which is not tied to the normal scrollback/logical line list.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND <html>(, <ignored>)`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<ignored>` (optional): integer expression. Accepted by the argument parser but ignored by this instruction.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string and appends the rendered HTML output into a separate “island” layer.
- The island layer is not counted by `LINECOUNT` and is not removed by `CLEARLINE`.
- The island layer is drawn independently of the normal log:
  - It does not scroll with the log.
  - It is drawn from the top of the window, with each appended “logical line” placed on successive rows.
- Note: `<div ...>...</div>` sub-areas are not rendered in the island layer.
- Use `HTML_PRINT_ISLAND_CLEAR` to clear the island layer.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
HTML_PRINT_ISLAND "<div width='300px' height='30px' color='#202020'><font color='white'>Status</font></div>"
```

**Progress state**
- complete
