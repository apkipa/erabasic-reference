**Summary**
- Draws a horizontal rule by repeating a raw pattern string across the drawable width, then prints a newline.

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
  - Measure is based on rendered display width (using the configured default font and `DrawableWidth`).
  - Repeats `<pattern>` until the measured width reaches/exceeds `DrawableWidth`, then removes characters from the end until it fits.
- Prints the expanded bar with font style forced to `Regular`, then prints a newline.

**Errors & validation**
- Load-time error if `<pattern>` is omitted.

**Examples**
- `CUSTOMDRAWLINE -`
- `CUSTOMDRAWLINE =*=`

**Progress state**
- complete
