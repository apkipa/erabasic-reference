**Summary**
- A “forced quit” instruction in this engine build.

**Tags**
- system

**Syntax**
- `FORCE_QUIT`

**Arguments**
- None.

**Semantics**
- In the current engine implementation, this instruction does not request a normal quit by itself.
- It participates in the same “consecutive forced restart” guard used by `FORCE_QUIT_AND_RESTART`.

**Errors & validation**
- May raise a runtime error on the guard path (see `FORCE_QUIT_AND_RESTART`).

**Examples**
- `FORCE_QUIT`

**Progress state**
- complete
