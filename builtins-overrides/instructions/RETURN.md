**Summary**
- Returns from the current function. Also assigns the integer `RESULT` array (`RESULT:0`, `RESULT:1`, ...) from the provided values.

**Tags**
- calls

**Syntax**
- `RETURN`
- `RETURN <int expr1> [, <int expr2>, <int expr3>, ... ]`

**Arguments**
- Each argument is evaluated as an integer and stored into `RESULT:<index>`.

- Omitted arguments / defaults:
  - With no arguments: sets `RESULT:0` to `0` and returns `0`.

**Semantics**
- Evaluates all provided integer expressions (left-to-right), stores them into the `RESULT` integer array starting at index 0, then returns from the function.
- The return value used by the call stack is `RESULT:0` after the assignment.
- The engine does not clear unused `RESULT:<index>` slots; old values past the written prefix may remain.
- Load-time diagnostics (non-fatal): the engine may emit compatibility warnings when `RETURN` is used with a non-constant expression/variable, or with multiple values.

**Errors & validation**
- Errors if any argument cannot be evaluated as an integer.

**Examples**
- `RETURN`
- `RETURN 0`
- `RETURN 1, 2, 3`

**Progress state**
- complete
