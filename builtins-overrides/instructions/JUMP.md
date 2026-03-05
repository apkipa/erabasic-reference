**Summary**
- Jumps into another non-event function (`@NAME`) like `CALL`, but does not return to the current function.

**Tags**
- calls

**Syntax**
- `JUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `JUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

**Semantics**
- Enters the target function.
- When the target function returns, the engine immediately returns again, effectively discarding the current function’s return address (tail-call-like behavior).

**Errors & validation**
- Same as `CALL`.

**Examples**
- `JUMP NEXT_PHASE`

**Progress state**
- complete
