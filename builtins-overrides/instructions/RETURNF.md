**Summary**
- Returns from a user-defined expression function (`#FUNCTION/#FUNCTIONS`) with an optional return value.

**Tags**
- calls

**Syntax**
- `RETURNF`
- `RETURNF <expr>`

**Arguments**
- `<expr>` (optional): expression whose type should match the function’s declared return type.


**Semantics**
- Sets the method return value for the current expression-function call and exits the method body.
- If `<expr>` is omitted:
  - int-returning method: returns `0`
  - string-returning method: returns `""`
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
