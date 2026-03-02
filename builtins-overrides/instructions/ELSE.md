**Summary**
- Final clause header inside an `IF ... ENDIF` block.

**Syntax**
- `ELSE`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- When reached **sequentially**, `ELSE` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When selected by the `IF` header, the engine jumps to the `ELSE` line as a **marker** and begins executing at the next line (the `ELSE` body).

**Errors & validation**
- Invalid placement (outside `IF`) produces a load-time warning.
- `ELSEIF` or `ELSE` after an `ELSE` produces a load-time warning.

**Examples**
- `ELSE`
