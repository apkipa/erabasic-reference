**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- save-system

**Syntax**
- `LOADVAR <name>`

**Arguments**
- `<name>`: string expression; intended file name component.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Always errors at runtime.

**Examples**
- `LOADVAR "vars"`

**Progress state**
- complete
