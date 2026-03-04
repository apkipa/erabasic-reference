**Summary**
- Ends a `TRY*LIST ... ENDFUNC` block.

**Tags**
- functions

**Syntax**
- `ENDFUNC`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The surrounding `TRY*LIST` uses it as the jump target when no candidate succeeds.

**Errors & validation**
- `ENDFUNC` without a matching open `TRY*LIST` is a load-time error (the line is marked as error).

**Examples**
- `ENDFUNC`

**Progress state**
- complete
