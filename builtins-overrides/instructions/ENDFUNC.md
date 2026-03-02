**Summary**
- Ends a `TRY*LIST ... ENDFUNC` block.

**Syntax**
- `ENDFUNC`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The surrounding `TRY*LIST` uses it as the jump target when no candidate succeeds.

**Errors & validation**
- `ENDFUNC` without a matching open `TRY*LIST` produces a load-time warning.

**Examples**
- `ENDFUNC`
