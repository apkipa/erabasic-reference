**Summary**
- Returns from the current function like `RETURN`, but parses its values from a FORM/formatted string.

**Syntax**
- `RETURNFORM <formString>`

**Arguments**
- `<formString>` is evaluated to a string, then that string is re-lexed as one or more **comma-separated integer expressions**.

**Defaults / optional arguments**
- If the string yields no expressions, the engine behaves like `RETURN 0`.

**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Stores the resulting integer values into `RESULT:0..` and returns.

**Errors & validation**
- Errors if any parsed expression is not a valid integer expression.

**Examples**
- `RETURNFORM "1, 2, %A%"`
