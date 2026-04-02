**Summary**
- Returns from the current function like `RETURN`, but parses its values from a FORM/formatted string.

**Tags**
- calls

**Syntax**
- `RETURNFORM <formString>`

**Arguments**
- `<formString>` is evaluated to a string `s`, then `s` is re-lexed as one or more **comma-separated integer expressions**.


**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Parsing detail: after each comma, the engine skips ASCII spaces (not tabs) before reading the next expression.
- Stores the resulting integer values into `RESULT:0`, `RESULT:1`, ... and returns.
- If `s` is empty, behaves like `RETURN 0`.

**Errors & validation**
- Errors if any parsed expression is not a valid integer expression.
- `RETURNFORM` inside a user-defined expression-function body (`#FUNCTION` / `#FUNCTIONS`) is a load-time error (the line is marked as error), because `RETURNFORM` is not method-safe there; use `RETURNF` instead.

**Examples**
- `RETURNFORM 1, 2, {A}`

**Progress state**
- complete
