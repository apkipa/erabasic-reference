**Summary**
- Returns the name of the currently executing parent label/function.

**Tags**
- runtime
- reflection

**Syntax**
- `GETDOINGFUNCTION()`

**Signatures / argument rules**
- `GETDOINGFUNCTION()` → `string`

**Arguments**
- None.

**Semantics**
- Returns the current scanning line's parent label name.
- Returns `""` if there is no active running function context, for example from a system-wait debug context.

**Errors & validation**
- None.

**Examples**
- `fn = GETDOINGFUNCTION()`

**Progress state**
- complete
