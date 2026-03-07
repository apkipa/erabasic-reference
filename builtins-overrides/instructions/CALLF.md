**Summary**
- Calls an expression function (built-in method or user-defined `#FUNCTION/#FUNCTIONS`) by name and evaluates it as a statement.

**Tags**
- calls

**Syntax**
- `CALLF <methodName>`
- `CALLF <methodName>()`
- `CALLF <methodName>, <arg1> [, <arg2> ... ]`
- `CALLF <methodName>(<arg1> [, <arg2> ... ])`
- `CALLF <methodName>[<subName1>, <subName2>, ...]`
- `CALLF <methodName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<methodName>` (raw string token): read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<methodName>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

**Semantics**
- Resolves `<methodName>` to an expression function and evaluates it with the provided arguments.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction (use statement-form method calls or assignment if you need the value).

**Errors & validation**
- If `<methodName>` is a constant string: unknown methods are a load-time error (the line is marked as error).
- Errors if the method exists but argument checking fails.

**Examples**
- `CALLF MYFUNC, 1, 2`

**Progress state**
- complete
