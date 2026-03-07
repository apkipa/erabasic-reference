**Summary**
- Calls a non-event script function (`@NAME`) and returns to the next line after the `CALL` when the callee returns.

**Tags**
- calls

**Syntax**
- `CALL <functionName>`
- `CALL <functionName>()`
- `CALL <functionName>, <arg1> [, <arg2> ... ]`
- `CALL <functionName>(<arg1> [, <arg2> ... ])`
- `CALL <functionName>[<subName1>, <subName2>, ...]`
- `CALL <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<functionName>` (raw string token): read up to `(` / `[` / `,` / `;` and then trimmed.
  - This is **not** a string literal. Quotes are treated as ordinary characters.
  - Backslash escapes are processed (e.g. `\n`, `\t`, `\s`).
- `<argN>` (optional, expression): each occurrence is evaluated, passed to the callee, and bound to its `ARG`/`ARGS`-based parameters and/or `#FUNCTION` parameter declarations.
- `<subNameN>` (optional): values parsed from the bracket segment after `<functionName>`.
  - The current engine accepts and stores them, but they do not affect target resolution or call behavior.

**Semantics**
- Resolves the target label to a non-event function.
  - If `CompatiCallEvent` is enabled, an event function name is also callable via `CALL` (compatibility behavior: it calls only the first-defined function, ignoring event priority/single flags).
- Evaluates arguments, binds them to the callee’s declared formals (including `REF` behavior), then enters the callee.
- When the callee executes `RETURN` (or reaches end-of-function), control returns to the statement after the `CALL`.
- Load-time behavior: if `<functionName>` is a compile-time constant, the loader resolves the callee during load and may emit early diagnostics (e.g. unknown function, argument binding issues).

**Errors & validation**
- If `<functionName>` is a constant string:
  - Non-`TRY*` variants: an unknown function is a load-time error (the line is marked as error).
  - `TRY*` variants: an unknown function is allowed (the line is not marked as error).
- Errors if the function exists but is not callable by `CALL`:
  - event function name when `CompatiCallEvent` is disabled
  - user-defined expression function (`#FUNCTION/#FUNCTIONS`)
- Errors if argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.).

**Examples**
- `CALL TRAIN_MAIN, TARGET`
- `CALL SHOP_MAIN()`

**Progress state**
- complete
