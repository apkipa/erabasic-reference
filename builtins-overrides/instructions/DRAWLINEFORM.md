**Summary**
- Draws a horizontal rule by repeating a runtime string expression across the derived runtime value `DrawableWidth`, then prints a newline.

**Tags**
- ui

**Syntax**
- `DRAWLINEFORM <pattern>`

**Arguments**
- `<pattern>` (string): pattern to repeat.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Evaluates `<pattern>` to a string `s`.
  - If `s` is non-empty, expands it to a full-width bar using the same algorithm as `CUSTOMDRAWLINE`, which fits the pattern to the derived runtime value `DrawableWidth` (see `config-items.md`).
- Prints the expanded bar with font style forced to `Regular`, then prints a newline.

**Errors & validation**
- Runtime error if `<pattern>` evaluates to `""` (empty).

**Examples**
- `DRAWLINEFORM "-" + STRFORM("%02d", RAND:100)`

**Progress state**
- complete
