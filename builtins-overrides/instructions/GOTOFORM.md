**Summary**
- Like `GOTO`, but the label name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `GOTOFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the `$label` name.

**Semantics**
- Evaluates the label name and jumps if it resolves to a `$label` in the current function.

**Errors & validation**
- Same as `GOTO`, but errors may occur at runtime if the evaluated label name varies.

**Examples**
- `GOTOFORM "CASE_%RESULT%"`

**Progress state**
- complete
