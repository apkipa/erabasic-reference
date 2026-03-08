**Summary**
- Tests whether a user-defined in-expression function is callable with zero arguments.

**Tags**
- reflection

**Syntax**
- `EXISTMETH(name)`

**Signatures / argument rules**
- `EXISTMETH(name)` → `long`

**Arguments**
- `name` (string): target method name.

**Semantics**
- Resolves only user-defined in-expression functions/methods.
- Built-in expression functions are not searched here.
- Resolution is attempted with zero forwarded call arguments.
- Returns `0` if:
  - no matching user-defined method is found,
  - the same-name label is not a method,
  - or zero-argument resolution fails.
- Otherwise returns a bitmask describing the resolved zero-arg callable result type:
  - `1`: callable as integer,
  - `2`: callable as string,
  - `3`: supports both.

**Errors & validation**
- None; resolution failures collapse to `0`.

**Examples**
- `kind = EXISTMETH("MYSCORE")`

**Progress state**
- complete
