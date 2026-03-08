**Summary**
- Resets global variables to their default values.

**Tags**
- save-system

**Syntax**
- `RESETGLOBAL`

**Arguments**
- None.

**Semantics**
- Resets built-in `GLOBAL/GLOBALS` and ERH `GLOBAL` user-defined variables to their default values.
- Removes Emuera-private global/static extension data (e.g. XML/maps global/static extensions).
- Does not touch local stores, non-global variables, or the current character list.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETGLOBAL`

**Progress state**
- complete
