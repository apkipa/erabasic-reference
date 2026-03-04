**Summary**
- Returns from a user-defined expression function (`#FUNCTION/#FUNCTIONS`) with an optional return value.

**Tags**
- calls

**Syntax**
- `RETURNF`
- `RETURNF <expr>`

**Arguments**
- `<expr>` may be int or string, but should match the function’s declared return type.

- Omitted arguments / defaults:
  - With no argument: returns the engine’s “null” method value (a null internal return term; typically treated as `0` / empty depending on context).

**Semantics**
- Sets the method return value for the current expression-function call and exits the method body.
- Load-time validation:
  - `RETURNF` outside a `#FUNCTION/#FUNCTIONS` body is a load-time error (the line is marked as error).
  - A return-type mismatch (`RETURNF` returns string from an int method, or int from a string method) is a load-time error.

**Errors & validation**
- Argument parsing errors follow normal expression parsing rules.

**Examples**
- `RETURNF 0`
- `RETURNF "OK"`

**Progress state**
- complete
