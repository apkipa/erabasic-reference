**Summary**
- Final clause header inside an `IF ... ENDIF` block.

**Tags**
- control-flow

**Syntax**
- `ELSE`

**Arguments**
- None.

**Semantics**
- When reached **sequentially**, `ELSE` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When selected by the `IF` header, the engine jumps to the `ELSE` line as a **marker** and begins executing at the next line (the `ELSE` body).

**Errors & validation**
- Invalid placement (outside `IF`) is a load-time error (the line is marked as error).
- `ELSEIF` or `ELSE` after an `ELSE` produces a load-time warning.

**Examples**
- `ELSE`

**Progress state**
- complete
