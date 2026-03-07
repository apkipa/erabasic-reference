**Summary**
- Deletes every currently registered character.

**Tags**
- characters

**Syntax**
- `DELALLCHARA`

**Arguments**
- None.

**Semantics**
- Removes all characters from the current character list.
- After completion, `CHARANUM` becomes `0`.
- The instruction is safe when the list is already empty.
- It does **not** automatically rewrite `MASTER`, `TARGET`, or `ASSI`; scripts that rely on those variables must reset or re-check them afterward.

**Errors & validation**
- None.

**Examples**
- `DELALLCHARA`

**Progress state**
- complete
