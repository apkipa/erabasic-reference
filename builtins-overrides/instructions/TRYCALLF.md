**Summary**
- Tries to call a **user-defined** expression function (`#FUNCTION/#FUNCTIONS`) by name; if it cannot be resolved, does nothing.

**Tags**
- calls

**Syntax**
- `TRYCALLF <methodName> [, <arg1>, <arg2>, ... ]`
- `TRYCALLF <methodName>(<arg1>, <arg2>, ... )`
- Optional (currently unused) bracket segment may appear after the name:
  - `TRYCALLF <methodName>[<subName1>, <subName2>, ...](...)`

**Arguments**
- `<methodName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
  - This is **not** a string literal or string expression.
  - Quotes are treated as ordinary characters.
  - Backslash escapes are processed (e.g. `\\n`, `\\t`, `\\s`).
- `<argN>`: expressions passed to the target method.

**Semantics**
- Resolution scope:
  - Only **user-defined** expression functions are considered (built-in expression functions are not).
- Resolves `<methodName>` to a user-defined expression function with the provided argument list.
  - If no matching method is found (or it cannot be resolved at load time for the constant-name fast path), the instruction is a no-op.
  - Otherwise evaluates the method.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- The “try” behavior only covers “cannot resolve to a callable user-defined expression function”.
- Errors if a name resolves to an incompatible kind of function (not an expression function) or if argument checking/conversion fails.

**Examples**
- `TRYCALLF HOOK_AFTER_PRINT, TARGET`

**Progress state**
- complete
