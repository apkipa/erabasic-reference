**Summary**
- Calls an expression function (built-in method or user-defined `#FUNCTION/#FUNCTIONS`) by name and evaluates it as a statement.

**Syntax**
- `CALLF <methodName> [, <arg1>, <arg2>, ... ]`
- `CALLF <methodName>(<arg1>, <arg2>, ... )`

**Arguments**
- `<methodName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>`: expressions passed to the method.

**Defaults / optional arguments**
- Depends on the called method’s own signature rules (omission/variadics/etc.).

**Semantics**
- Resolves `<methodName>` to an expression function and evaluates it with the provided arguments.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction (use statement-form method calls or assignment if you need the value).

**Errors & validation**
- Errors if the method does not exist or if argument checking fails.

**Examples**
- `CALLF "MYFUNC", 1, 2`
