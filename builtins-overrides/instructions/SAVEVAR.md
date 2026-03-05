**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- save-system

**Syntax**
- `SAVEVAR <name>, <saveText>, <var1> [, <var2> ...]`

**Arguments**
- `<name>`: string expression; intended file name component.
- `<saveText>`: string expression; intended description text.
- `<var*>`: one or more changeable non-character variable terms (arrays are allowed; several variable categories are rejected).

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Always errors at runtime.

**Examples**
- `SAVEVAR "vars", "checkpoint", A, B, C`

**Progress state**
- complete
