**Summary**
- Sets one or more bits in a writable integer variable.

**Tags**
- math

**Syntax**
- `SETBIT <integerVariable>, <bit1> [, <bit2> ... ]`

**Arguments**
- `<integerVariable>` (writable int variable): target variable.
- `<bitN>` (int): bit position; each value must satisfy `0 <= bit <= 63`.

**Semantics**
- Evaluates the bit arguments left-to-right.
- For each evaluated bit `b`, immediately updates `<integerVariable>` with `value |= (1 << b)`.
- The variable is reread before each step, so later bit expressions observe earlier mutations if they read the same variable.
- Duplicate bit positions are allowed; the same bit may be processed more than once in one call.

**Errors & validation**
- Parse / argument-validation error if `<integerVariable>` is missing, is not a writable int variable, or no bit argument is supplied.
- Parse / argument-validation error if a constant `<bitN>` is outside `0 <= bit <= 63`.
- Runtime error if an evaluated `<bitN>` is outside `0 <= bit <= 63`.
- If a later bit errors at runtime, earlier bit changes remain.

**Examples**
- `SETBIT FLAG, 0`
- `SETBIT FLAGS, 1, 3, 5`

**Progress state**
- complete
