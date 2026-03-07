**Summary**
- Sets the console’s “message skip” flag (`MesSkip`), which affects UI-side input handling and macro/skip behavior.
- This is **not** the same mechanism as `SKIPDISP` (which skips print-family instructions in the script runner).

**Tags**
- skip-mode

**Syntax**
- `SKIPLOG <enabled>`

**Arguments**
- `<enabled>` (int): `0` clears message-skip; non-zero enables message-skip.

**Semantics**
- Evaluates `<enabled>` to `v`.
- Sets the message-skip flag `MesSkip` to `(v != 0)`.
- Implementation-oriented effect (UI-side):
  - When `MesSkip` is true, the input loop may automatically advance through waits that do not require a value, unless the current wait request explicitly stops message skip.
  - Some input instructions (`INPUT*`/`TINPUT*`) have a `canSkip` option that uses `MesSkip` to auto-accept their default value without waiting.

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `SKIPLOG 1`
- `SKIPLOG 0`

**Progress state**
- complete
