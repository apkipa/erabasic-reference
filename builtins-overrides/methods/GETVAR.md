**Summary**
- Parses a string as an integer variable term and returns its current value.

**Tags**
- reflection

**Syntax**
- `GETVAR(varExpr)`

**Signatures / argument rules**
- `GETVAR(varExpr)` → `long`

**Arguments**
- `varExpr` (string): text that must parse to an integer variable term.

**Semantics**
- Re-parses `varExpr` at runtime using the normal expression parser.
- `varExpr` must reduce to a variable term.
- Constants are allowed.
- Array elements are allowed if `varExpr` includes valid subscripts.
- Scope-sensitive names (for example locals/private variables) follow the current runtime context exactly as if the same variable term had appeared directly in script code.

**Errors & validation**
- Runtime error if `varExpr` does not parse to a variable term.
- Runtime error if the resolved term is not integer-typed.
- Runtime error if normal variable evaluation of that term fails.

**Examples**
- `value = GETVAR("TARGET")`
- `value = GETVAR("ARRAY:3")`

**Progress state**
- complete
