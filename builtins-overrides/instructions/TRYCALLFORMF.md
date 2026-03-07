**Summary**
- Like `TRYCALLF`, but the method name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `TRYCALLFORMF <formString>`
- `TRYCALLFORMF <formString>()`
- `TRYCALLFORMF <formString>, <arg1> [, <arg2> ... ]`
- `TRYCALLFORMF <formString>(<arg1> [, <arg2> ... ])`
- `TRYCALLFORMF <formString>[<subName1>, <subName2>, ...]`
- `TRYCALLFORMF <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<formString>` (FORM/formatted string): its evaluated result is used as the method name.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the target method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<formString>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

**Semantics**
- Evaluates `<formString>` to a name string, then behaves like `TRYCALLF`.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- Same as `TRYCALLF`.

**Examples**
- `TRYCALLFORMF "HOOK_%TARGET%", TARGET`

**Progress state**
- complete
