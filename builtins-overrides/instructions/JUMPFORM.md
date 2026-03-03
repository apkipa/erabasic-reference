**Summary**
- Like `JUMP`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Syntax**
- `JUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `JUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
- Same as `CALLFORM`.

**Semantics**
- Same as `JUMP`, with a runtime-evaluated function name.

**Errors & validation**
- Same as `JUMP`, but errors may occur at runtime if the evaluated function name varies.

**Examples**
- `JUMPFORM "EVENT_%COUNT%"`

**Progress state**
- complete
