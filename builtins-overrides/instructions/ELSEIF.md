**Summary**
- Clause header inside an `IF ... ENDIF` block.

**Syntax**
- `ELSEIF <int expr>`

**Arguments**
- `<int expr>` is evaluated by the `IF` header’s clause-selection logic (not by the `ELSEIF` instruction itself).

**Defaults / optional arguments**
- None.

**Semantics**
- When reached **sequentially** (i.e., a previous clause already executed and control fell through), `ELSEIF` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When entered as the selected clause, the engine jumps to the `ELSEIF` line as a **marker** and begins executing at the next line (the clause body); the `ELSEIF` instruction itself is not executed in that path.

**Errors & validation**
- Invalid placement (outside `IF`) produces a load-time warning.

**Examples**
- `ELSEIF A > 10`
