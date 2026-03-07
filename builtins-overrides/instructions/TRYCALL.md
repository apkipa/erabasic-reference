**Summary**
- Like `CALL`, but if the target function does not exist the instruction **does not error** and simply falls through to the next line.

**Tags**
- calls

**Syntax**
- `TRYCALL <functionName>`
- `TRYCALL <functionName>()`
- `TRYCALL <functionName>, <arg1> [, <arg2> ... ]`
- `TRYCALL <functionName>(<arg1> [, <arg2> ... ])`
- `TRYCALL <functionName>[<subName1>, <subName2>, ...]`
- `TRYCALL <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- Same as `CALL`.

**Semantics**
- If the target function exists: behaves like `CALL`.
- If the target function does not exist: does nothing (continues at the next line after `TRYCALL`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYCALL OPTIONAL_HOOK`

**Progress state**
- complete
