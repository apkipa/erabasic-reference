**Summary**
- Dynamically calls a user-defined numeric in-expression function by name.

**Tags**
- reflection

**Syntax**
- `GETMETH(name [, defaultValue [, args ...]])`

**Signatures / argument rules**
- `GETMETH(name)` → `long`
- `GETMETH(name, defaultValue)` → `long`
- `GETMETH(name, defaultValue [, args ...])` → `long`

**Arguments**
- `name` (string): target method name.
- `defaultValue` (optional, int): fallback return used only when no matching user-defined method is found.
- `args...` (optional, any): arguments forwarded to the resolved target method.

**Semantics**
- Resolves only user-defined in-expression functions/methods.
- Built-in expression functions are not searched here.
- `defaultValue` is a reserved fallback slot and is **not** forwarded to the target call.
  - To pass call arguments without a fallback, omit that slot explicitly.
- If no matching user-defined method is found:
  - returns `defaultValue` when it is present,
  - otherwise raises a runtime error.
- If a same-name script label exists but is not a method, this is an error, not a `not found` fallback case.
- If a matching method exists but the forwarded arguments are invalid, this is an error, not a fallback case.
- If a matching method exists but returns string type, this function raises a numeric-type mismatch error.

**Errors & validation**
- Runtime error when no method is found and `defaultValue` is omitted.
- Runtime error when the name resolves to a non-method script label.
- Runtime error when the resolved call fails argument validation.
- Runtime error when the resolved method is not integer-typed.

**Examples**
- `score = GETMETH("MYSCORE", 0, 1, 2)`

**Progress state**
- complete
