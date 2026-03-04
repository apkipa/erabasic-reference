**Summary**
- Returns from the current function like `RETURN`, but parses its values from a FORM/formatted string.

**Tags**
- calls

**Syntax**
- `RETURNFORM <formString>`

**Arguments**
- `<formString>` is evaluated to a string `s`, then `s` is re-lexed as one or more **comma-separated integer expressions**.

- Omitted arguments / defaults:
  - If `s` is empty, the engine behaves like `RETURN 0`.

**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Parsing detail: after each comma, the engine skips ASCII spaces (not tabs) before reading the next expression.
- Stores the resulting integer values into `RESULT:0`, `RESULT:1`, ... and returns.

**Errors & validation**
- Errors if any parsed expression is not a valid integer expression.

**Examples**
- `RETURNFORM 1, 2, %A%`

**Progress state**
- complete
