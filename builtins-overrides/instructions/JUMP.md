**Summary**
- Jumps into another non-event function (`@NAME`) like `CALL`, but does not return to the current function.

**Tags**
- calls

**Syntax**
- `JUMP <functionName>`
- `JUMP <functionName>()`
- `JUMP <functionName>, <arg1> [, <arg2> ... ]`
- `JUMP <functionName>(<arg1> [, <arg2> ... ])`
- `JUMP <functionName>[<subName1>, <subName2>, ...]`
- `JUMP <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
