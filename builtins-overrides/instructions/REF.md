**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- variables

**Syntax**
- `REF <refTarget>, <sourceName>`

**Arguments**
- `<refTarget>`: identifier token (intended to be a `REF` variable name; see `variables.md`).
- `<sourceName>`: identifier token naming the source variable to bind to.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- In this build, `REF` variables are still used by user-defined function argument binding (pass-by-reference); see `variables.md`.

**Errors & validation**
- Always errors at runtime.

**Examples**
- `REF X, A`

**Progress state**
- complete
