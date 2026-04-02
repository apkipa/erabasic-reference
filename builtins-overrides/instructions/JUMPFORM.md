**Summary**
- Like `JUMP`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `JUMPFORM <formString>`
- `JUMPFORM <formString>()`
- `JUMPFORM <formString>, <arg1> [, <arg2> ... ]`
- `JUMPFORM <formString>(<arg1> [, <arg2> ... ])`
- `JUMPFORM <formString>[<subName1>, <subName2>, ...]`
- `JUMPFORM <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- Same as `CALLFORM`.

**Semantics**
- Same as `JUMP`, with a runtime-evaluated function name.

**Errors & validation**
- Same as `JUMP`, but errors may occur at runtime if the evaluated function name varies.

**Examples**
- `JUMPFORM EVENT_{COUNT}`

**Progress state**
- complete
