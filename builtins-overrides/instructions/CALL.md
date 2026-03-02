**Summary**
- Calls a non-event script function (`@NAME`) and returns to the next line after the `CALL` when the callee returns.

**Syntax**
- `CALL <functionName> [, <arg1>, <arg2>, ... ]`
- `CALL <functionName>(<arg1>, <arg2>, ... )`
- Optional (currently unused) bracket segment may appear after the function name:
  - `CALL <functionName>[<subName1>, <subName2>, ...](...)`

**Arguments**
- `<functionName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>`: expressions passed to the callee and bound to its `ARG`/`ARGS`-based parameters and/or `#FUNCTION` parameter declarations.

**Defaults / optional arguments**
- If the callee declares more parameters than provided arguments, omitted arguments are handled by the engine’s user-function argument binder (defaults and config gates apply).

**Semantics**
- Resolves the target label to a non-event function. Calling an event function by name is rejected unless compatibility config allows it.
- Evaluates arguments, binds them to the callee’s declared formals (including `REF` behavior), then enters the callee.
- When the callee executes `RETURN` (or reaches end-of-function), control returns to the statement after the `CALL`.

**Errors & validation**
- Errors if the function does not exist, if it is an event function (when not permitted), or if it is a user-defined expression function (`#FUNCTION/#FUNCTIONS`).
- Errors if argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.).

**Examples**
- `CALL TRAIN_MAIN, TARGET`
- `CALL SHOP_MAIN()`
