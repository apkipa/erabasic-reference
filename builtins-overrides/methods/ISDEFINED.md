**Summary**
- Tests whether a macro is currently defined.

**Tags**
- reflection

**Syntax**
- `ISDEFINED(name)`

**Signatures / argument rules**
- `ISDEFINED(name)` → `long`

**Arguments**
- `name` (string): macro name.

**Semantics**
- Returns `1` if a macro with that name exists in the current macro table.
- Returns `0` otherwise.
- This function checks macros only. It does not test variables, labels, or methods.
- Name matching follows the runtime's normal macro-lookup rules.

**Errors & validation**
- None.

**Examples**
- `ISDEFINED("MY_MACRO")`

**Progress state**
- complete
