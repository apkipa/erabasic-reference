**Summary**
- Returns from a user-defined expression function (`#FUNCTION/#FUNCTIONS`) with an optional return value.

**Syntax**
- `RETURNF`
- `RETURNF <expr>`

**Arguments**
- `<expr>` may be int or string, but should match the function’s declared return type.

**Defaults / optional arguments**
- With no argument: returns the engine’s “null” method value (treated as 0 / empty depending on context).

**Semantics**
- Sets the method return value for the current expression-function call and exits the method body.
- Load-time validation warns if used outside a method function, and warns on obvious return-type mismatch.

**Errors & validation**
- Argument parsing errors follow normal expression parsing rules.

**Examples**
- `RETURNF 0`
- `RETURNF "OK"`
