**Summary**
- Tests whether a bare variable name resolves, and returns a bitmask describing its declared shape/type.

**Tags**
- reflection

**Syntax**
- `EXISTVAR(name)`

**Signatures / argument rules**
- `EXISTVAR(name)` → `long`

**Arguments**
- `name` (string): bare variable name.

**Semantics**
- Resolves `name` as a variable token, not as a full variable-term expression.
  - Subscripted strings such as `A:0` are not parsed here.
- Scope lookup follows the runtime's normal variable-token rules:
  - current private variable first,
  - then local variable,
  - then global/system variable.
- Returns `0` if no variable token is found.
- Otherwise returns a bitmask with these flags:
  - `1`: integer-typed
  - `2`: string-typed
  - `4`: const
  - `8`: 2D array
  - `16`: 3D array
- No flag distinguishes scalar from 1D array.
- No flag distinguishes ordinary variables from character-data variables.

**Errors & validation**
- Some names can still raise runtime errors instead of returning `0` when normal variable-token lookup would reject them, for example prohibited variables or local/private lookups with no valid current function context.

**Examples**
- `mask = EXISTVAR("TARGET")`

**Progress state**
- complete
