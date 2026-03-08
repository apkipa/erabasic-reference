**Summary**
- Like `GETNUM`, but takes the variable name as a string instead of a variable term.

**Tags**
- string-key
- erd

**Syntax**
- `GETNUMB(varName, key)`

**Signatures / argument rules**
- `GETNUMB(varName, key)` → `long`

**Arguments**
- `varName` (string): variable name to resolve at runtime (for example `"ABL"`, `"CALLNAME"`, or a user-defined variable name).
- `key` (string): key name to resolve.

**Semantics**
- Resolves `varName` to a variable token at runtime.
- Then performs the same lookup model as `GETNUM`:
  - built-in CSV-name / alias dictionary first,
  - ERD fallback second (using only the base variable name, because this function has no `dimension` argument).
- Returns the mapped integer index on success; otherwise returns `-1`.
- `key = ""` also returns `-1`.

**Errors & validation**
- Runtime error if `varName` does not resolve to a variable name in the current runtime.
- No runtime error is raised merely because the resolved variable family has no key dictionary; that case returns `-1`.

**Examples**
- `n = GETNUMB("ABL", "技巧")`

**Progress state**
- complete
