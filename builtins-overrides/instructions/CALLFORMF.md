**Summary**
- Like `CALLF`, but the method name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `CALLFORMF <formString>`
- `CALLFORMF <formString>()`
- `CALLFORMF <formString>, <arg1> [, <arg2> ... ]`
- `CALLFORMF <formString>(<arg1> [, <arg2> ... ])`
- `CALLFORMF <formString>[<subName1>, <subName2>, ...]`
- `CALLFORMF <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<formString>` (FORM/formatted string): its evaluated result is used as the method name.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<formString>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

**Semantics**
- Resolves the evaluated name to an expression function and evaluates it.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- Errors if the method does not exist or if argument checking fails.

**Examples**
- `CALLFORMF "FUNC_%X%", A, B`

**Progress state**
- complete
