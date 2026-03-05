**Summary**
- Sets the current background color by a named color.

**Tags**
- ui

**Syntax**
- `SETBGCOLORBYNAME <name>`

**Arguments**
- `<name>` (raw string): a color name recognized by `System.Drawing.Color.FromName`.
  - This is a raw string argument, not a string expression.

**Semantics**
- Resolves `<name>` via `Color.FromName(name)` and sets the background color to the resolved RGB.
- Does not print output.

**Errors & validation**
- Parse-time error if `<name>` is not a valid color name.
- Parse-time error if `<name>` is `"transparent"` (case-insensitive).

**Examples**
- `SETBGCOLORBYNAME Black`

**Progress state**
- complete

