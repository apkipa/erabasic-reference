**Summary**
- Draws a horizontal rule by repeating a raw pattern string across the derived runtime value `DrawableWidth`, then prints a newline.

**Tags**
- ui

**Syntax**
- `CUSTOMDRAWLINE <pattern>`

**Arguments**
- `<pattern>` (raw text): the remainder of the line after the keyword.
  - This is not an expression.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Expands `<pattern>` to a full-width bar using the engine’s “custom bar” algorithm:
  - Measure is based on rendered display width using the configured default font and the derived runtime value `DrawableWidth` (see `config-items.md`).
  - Repeats `<pattern>` until the measured width reaches/exceeds that width, then removes characters from the end until it fits.
- Prints the expanded bar with font style forced to `Regular`, then prints a newline.

**Errors & validation**
- Load-time error if `<pattern>` is omitted.

**Examples**
- `CUSTOMDRAWLINE -`
- `CUSTOMDRAWLINE =*=`

**Progress state**
- complete
