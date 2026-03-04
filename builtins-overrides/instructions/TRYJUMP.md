**Summary**
- Like `JUMP`, but if the target function does not exist the instruction **does not error** and simply falls through to the next line.

**Tags**
- calls

**Syntax**
- `TRYJUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYJUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMP`.

- Omitted arguments / defaults:
  - Same as `JUMP`.

**Semantics**
- If the target function exists: behaves like `JUMP`.
- If the target function does not exist: does nothing (continues at the next line after `TRYJUMP`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYJUMP OPTIONAL_PHASE`

**Progress state**
- complete
