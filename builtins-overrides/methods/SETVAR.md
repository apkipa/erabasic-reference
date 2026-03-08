**Summary**
- Parses a string as a writable variable term and assigns one value to it.

**Tags**
- reflection

**Syntax**
- `SETVAR(varExpr, value)`

**Signatures / argument rules**
- `SETVAR(varExpr, value)` → `long`

**Arguments**
- `varExpr` (string): text that must parse to a writable variable term.
- `value` (int|string): value to assign; its type must match the resolved variable type.

**Semantics**
- Re-parses `varExpr` at runtime using the normal expression parser.
- `varExpr` must reduce to a non-const variable term.
- The assignment target can be a scalar variable or one addressed array element.
- If the resolved target is string-typed, `value` must be string-typed.
- If the resolved target is integer-typed, `value` must be integer-typed.
- Returns `1` after a successful assignment.

**Errors & validation**
- Runtime error if `varExpr` does not parse to a writable variable term.
- Runtime error if the resolved target is const.
- Runtime error if `value` has the wrong type for the resolved target.
- Runtime error if normal target evaluation/assignment fails.

**Examples**
- `SETVAR("TARGET", 5)`
- `SETVAR("NAMES:3", "Alice")`

**Progress state**
- complete
