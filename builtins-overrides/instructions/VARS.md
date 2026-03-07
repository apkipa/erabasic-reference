**Summary**
- Declares a function-private dynamic string variable through the scoped-variable instruction extension.

**Tags**
- variables

**Syntax**
- `VARS <name>`
- `VARS <name> = "<literal>"`
- `VARS <name>, <size1>`
- `VARS <name>, <size1>, <size2>`
- `VARS <name>, <size1>, <size2>, <size3>`

**Arguments**
- `<name>` (string): private variable name declared in the containing function.
- `"<literal>"` (optional, double-quoted string literal): scalar initializer.
  - This is not a general string expression.
- `<size1>` (optional, int literal): first array size.
- `<size2>` (optional, int literal): second array size.
- `<size3>` (optional, int literal): third array size.
  - `VARS` supports 1D / 2D / 3D declarations.

**Semantics**
- Available only when `UseScopedVariableInstruction` is enabled; see `data-files.md` and `grammar.md`.
- At load time, `VARS` declares a function-private dynamic string variable in the containing function’s private-variable namespace.
- Name visibility is function-wide after load; other lines in the same function can resolve the variable name regardless of the declaration’s textual position.
- Executing the `VARS` line reinitializes that variable for the current call:
  - scalar form resets it, then applies the literal initializer if present
  - array form allocates a fresh empty-string-filled array of the declared size
- Re-executing the same `VARS` line during one call resets the variable again.
- On function return, the current call’s storage is discarded like other dynamic private variables.
- Array declarations do not have element initializers; if `= ...` text is present in an array form, it does not supply array contents.

**Errors & validation**
- Not available unless `UseScopedVariableInstruction` is enabled.
- Parse / load error if an array size is not an integer literal, if more than 3 dimensions are requested, or if the scalar initializer is not written as a double-quoted literal.
- Other name-validity rules follow ordinary function-private variable rules; see `variables.md`.

**Examples**
- `VARS QUESTION = "生命、宇宙、そして万物についての究極の疑問の答え"`
- `VARS BUFFER, 8`

**Progress state**
- complete
