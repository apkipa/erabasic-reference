**Summary**
- Declares a function-private dynamic int variable through the scoped-variable instruction extension.

**Tags**
- variables

**Syntax**
- `VARI <name>`
- `VARI <name> = <intValue>`
- `VARI <name>, <size1>`
- `VARI <name>, <size1>, <size2>`
- `VARI <name>, <size1>, <size2>, <size3>`

**Arguments**
- `<name>` (string): private variable name declared in the containing function.
- `<intValue>` (optional, int): scalar initializer.
- `<size1>` (optional, int literal): first array size.
- `<size2>` (optional, int literal): second array size.
- `<size3>` (optional, int literal): third array size.
  - `VARI` supports 1D / 2D / 3D declarations.

**Semantics**
- Available only when `UseScopedVariableInstruction` is enabled; see `data-files.md` and `grammar.md`.
- At load time, `VARI` declares a function-private dynamic int variable in the containing function’s private-variable namespace.
- Name visibility is function-wide after load; other lines in the same function can resolve the variable name regardless of the declaration’s textual position.
- Executing the `VARI` line reinitializes that variable for the current call:
  - scalar form resets it, then applies `<intValue>` if present
  - array form allocates a fresh zero-filled array of the declared size
- Re-executing the same `VARI` line during one call resets the variable again.
- On function return, the current call’s storage is discarded like other dynamic private variables.
- Array declarations do not have element initializers; if `= ...` text is present in an array form, it does not supply array contents.

**Errors & validation**
- Not available unless `UseScopedVariableInstruction` is enabled.
- Parse / load error if an array size is not an integer literal or if more than 3 dimensions are requested.
- Other name-validity rules follow ordinary function-private variable rules; see `variables.md`.

**Examples**
- `VARI ANSWER = 42`
- `VARI BUFFER, 16`

**Progress state**
- complete
