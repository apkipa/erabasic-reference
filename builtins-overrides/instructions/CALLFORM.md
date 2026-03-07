**Summary**
- Like `CALL`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `CALLFORM <formString>`
- `CALLFORM <formString>()`
- `CALLFORM <formString>, <arg1> [, <arg2> ... ]`
- `CALLFORM <formString>(<arg1> [, <arg2> ... ])`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the function name.
  - If this FORM expression constant-folds to a constant string, the engine treats it like `CALL` for load-time resolution.
- `<argN>` (optional): same as `CALL`.

**Semantics**
- Evaluates the function name string, resolves it to a non-event function, binds arguments, and enters the callee.

**Errors & validation**
- Same as `CALL`, but errors may occur at runtime if the evaluated function name varies.

**Examples**
- `CALLFORM "TRAIN_%TARGET%", TARGET`

**Progress state**
- complete
