**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- variables

**Syntax**
- `REFBYNAME <refTarget>, <sourceName>`

**Arguments**
- `<refTarget>`: identifier token (intended to be a `REF` variable name; see `variables.md`).
- `<sourceName>` (string expression): evaluates to a variable name string.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- In this build, `REF` variables are still used by user-defined function argument binding (pass-by-reference); see `variables.md`.

**Errors & validation**
- Always errors at runtime.

**Examples**
- `REFBYNAME X, "A"`

**Progress state**
- complete
